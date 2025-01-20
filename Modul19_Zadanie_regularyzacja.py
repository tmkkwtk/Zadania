import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping
from keras.regularizers import l2
import zipfile
from PIL import Image, UnidentifiedImageError
import shutil
import requests
import random

# Rozwiązanie problemu z OMP: dodanie zmiennych środowiskowych
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

# Funkcja do walidacji obrazów
def get_valid(file_path):
    correct_files = []
    for name in os.listdir(file_path):
        try:
            img = Image.open(os.path.join(file_path, name))
            correct_files.append(name)
        except UnidentifiedImageError:
            pass
    return correct_files

# Pobieranie i przygotowanie datasetu
url = "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip"
local_zip = 'cats-and-dogs.zip'
data_dir = 'data'

if not os.path.exists(data_dir):
    print("Pobieranie datasetu...")
    response = requests.get(url, stream=True)
    with open(local_zip, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

    del response

    print("Rozpakowywanie datasetu...")
    zip_ref = zipfile.ZipFile(local_zip, 'r')
    zip_ref.extractall(data_dir)
    zip_ref.close()
    print("Dataset gotowy.")
else:
    print("Dataset już istnieje.")

classes = ['Cat', 'Dog']
original_cat_path = os.path.join(data_dir, 'PetImages', 'Cat')
original_dog_path = os.path.join(data_dir, 'PetImages', 'Dog')
original_cat = get_valid(original_cat_path)
original_dog = get_valid(original_dog_path)

random.seed(101)
random.shuffle(original_cat)
random.shuffle(original_dog)

size = min(len(original_cat), len(original_dog))
train_size = int(np.floor(0.7 * size))
valid_size = int(np.floor(0.2 * size))
test_size = size - train_size - valid_size

base_directory = 'dataset'
if not os.path.exists(base_directory):
    os.mkdir(base_directory)
    type_datasets = ['train', 'valid', 'test']
    directories = {}

    for type_dataset in type_datasets:
        directory = os.path.join(base_directory, type_dataset)
        os.mkdir(directory)
        for name_class in classes:
            animal = os.path.join(directory, name_class)
            os.mkdir(animal)
            directories[f'{type_dataset}_{name_class}'] = animal + '/'

    index = 0
    for name_cat, name_dog in zip(original_cat, original_dog):
        if index <= train_size:
            type_of_dataset = 'train'
        elif train_size < index <= (train_size + valid_size):
            type_of_dataset = 'valid'
        elif (train_size + valid_size) < index <= (train_size + valid_size + test_size):
            type_of_dataset = 'test'
        shutil.copyfile(src=(os.path.join(original_cat_path, name_cat)), 
                        dst=(directories[f'{type_of_dataset}_Cat'] + name_cat))
        shutil.copyfile(src=(os.path.join(original_dog_path, name_dog)), 
                        dst=(directories[f'{type_of_dataset}_Dog'] + name_dog))
        index += 1

print(f'Dog - train: {len(os.listdir(os.path.join(base_directory, "train/Dog")))}\tCat - train: {len(os.listdir(os.path.join(base_directory, "train/Cat")))}')
print(f'Dog - valid: {len(os.listdir(os.path.join(base_directory, "valid/Dog")))}\tCat - valid: {len(os.listdir(os.path.join(base_directory, "valid/Cat")))}')
print(f'Dog - test:  {len(os.listdir(os.path.join(base_directory, "test/Dog")))}\tCat - test:  {len(os.listdir(os.path.join(base_directory, "test/Cat")))}')

# Dane i augmentacja
img_width, img_height = 150, 150
batch_size = 64
train_data_dir = 'dataset/train/'
validation_data_dir = 'dataset/valid/'

data_gen = ImageDataGenerator(rescale=1./255,
                               shear_range=0.2,
                               zoom_range=0.2,
                               rotation_range=30,
                               horizontal_flip=True)

train_generator = data_gen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

valid_gen = ImageDataGenerator(rescale=1./255)
validation_generator = valid_gen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

# Wspólne ustawienia
epochs = 50
steps_per_epoch = train_generator.samples // batch_size
validation_steps = validation_generator.samples // batch_size

# Early stopping
es = EarlyStopping(patience=5, monitor='val_loss', restore_best_weights=True)

# Funkcja do trenowania modeli
def train_and_evaluate(model, name):
    print(f"\nTrening modelu: {name}")
    history = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_steps,
        callbacks=[es])

    # Zapisywanie wyników
    model.save(f'{name}.h5')

    # Wykresy
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train')
    plt.plot(history.history['val_accuracy'], label='Validation')
    plt.title('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Validation')
    plt.title('Loss')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{name}_history.png')
    plt.show()

# Model z dodatkowymi warstwami i regularyzacją L2
model_l2 = Sequential()
model_l2.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3), kernel_regularizer=l2(0.01)))
model_l2.add(MaxPooling2D((2, 2)))
model_l2.add(Conv2D(64, (3, 3), activation='relu', kernel_regularizer=l2(0.01)))
model_l2.add(MaxPooling2D((2, 2)))
model_l2.add(Conv2D(128, (3, 3), activation='relu', kernel_regularizer=l2(0.01)))
model_l2.add(MaxPooling2D((2, 2)))
model_l2.add(Flatten())
model_l2.add(Dropout(0.5))
model_l2.add(Dense(256, activation='relu', kernel_regularizer=l2(0.01)))
model_l2.add(Dense(1, activation='sigmoid'))
model_l2.compile(optimizer=RMSprop(learning_rate=1e-4), loss='binary_crossentropy', metrics=['accuracy'])

train_and_evaluate(model_l2, "model_l2")

# Model z większą liczbą warstw konwolucyjnych i dropout
model_dropout = Sequential()
model_dropout.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)))
model_dropout.add(MaxPooling2D((2, 2)))
model_dropout.add(Conv2D(64, (3, 3), activation='relu'))
model_dropout.add(MaxPooling2D((2, 2)))
model_dropout.add(Conv2D(128, (3, 3), activation='relu'))
model_dropout.add(MaxPooling2D((2, 2)))
model_dropout.add(Conv2D(256, (3, 3), activation='relu'))
model_dropout.add(MaxPooling2D((2, 2)))
model_dropout.add(Flatten())
model_dropout.add(Dropout(0.5))
model_dropout.add(Dense(512, activation='relu'))
model_dropout.add(Dropout(0.5))
model_dropout.add(Dense(1, activation='sigmoid'))
model_dropout.compile(optimizer=RMSprop(learning_rate=1e-4), loss='binary_crossentropy', metrics=['accuracy'])

train_and_evaluate(model_dropout, "model_dropout")
