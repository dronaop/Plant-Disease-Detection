import tensorflow as tf
from keras.layers import Conv2D

# Define a custom Conv2D layer that removes the 'batch_input_shape' argument
def custom_conv2d(*args, **kwargs):
    kwargs.pop('batch_input_shape', None)  # Remove unsupported argument
    return Conv2D(*args, **kwargs)

print("Loading the model...")
# Load the model using the custom Conv2D
model = tf.keras.models.load_model('trained_model.keras', custom_objects={'Conv2D': custom_conv2d} , compile=False)

print("Saving the model in the SavedModel format...")
# Save the model in the SavedModel format
model.save('saved_model')

print("Model successfully converted!")