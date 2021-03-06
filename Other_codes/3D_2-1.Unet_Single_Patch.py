########################################################################################
# 3D Aorta Segmentation Project                                                        #
#                                                                                      #
# 2. 3D U-net                                                                          #
#                                                                                      #
# created by                                                                           #
# Shuai Chen                                                                           #
# PhD student                                                                          #
# Medical Informatics                                                                  #
#                                                                                      #
# P.O. Box 2040, 3000 CA Rotterdam, The Netherlands, internal postal address Na-2603   #
# Visiting address: office 2616, Wytemaweg 80, 3015 CN Rotterdam, The Netherlands      #
# Email s.chen.2@erasmusmc.nl | Telephone +31 6 334 516 99                             #
# www.erasmusmc.nl                                                                     #
#                                                                                      #
# created on 25/12/2017                                                                #
# Last update: 25/12/2017                                                              #
########################################################################################

from __future__ import print_function

import Modules.Common_modules as cm
import Modules.DenseUNet_3D as DenseUNet_3D
import Modules.UNet_3D as UNet_3D
import Modules.ResNet_3D as ResNet_3D
import Modules.LSTM_UNet_3D as LSTM_UNet_3D
import Modules.Callback as cb
import numpy as np
import datetime
from keras import callbacks
from keras.utils import plot_model
import sys


img_rows = cm.img_rows_3d
img_cols = cm.img_cols_3d
slices = cm.slices_3d
smooth = 1


def train_and_predict(use_existing):
  cm.mkdir(cm.workingPath.model_path)
  cm.mkdir(cm.workingPath.best_model_path)
  print('-' * 30)
  print('Loading and preprocessing train data...')
  print('-' * 30)

  # Choose which subset you would like to use:

  imgs_train = np.load(cm.workingPath.home_path + 'trainImages3D16.npy')
  imgs_mask_train = np.load(cm.workingPath.home_path + 'trainMasks3D16.npy')
  # imgs_train = np.load(cm.workingPath.home_path + 'trainImages3Dtest.npy')
  # imgs_mask_train = np.load(cm.workingPath.home_path + 'trainMasks3Dtest.npy')
  # imgs_train = np.load(cm.workingPath.trainingSet_path + 'trainImages_0000.npy')
  # imgs_mask_train = np.load(cm.workingPath.trainingSet_path + 'trainMasks_0000.npy')



  # imgs_val = np.load(cm.workingPath.validationSet_path + 'valImages3D.npy')
  # imgs_mask_val = np.load(cm.workingPath.validationSet_path + 'valMasks3D.npy')

  # imgs_train = np.load(cm.workingPath.training3DSet_path + 'trainImages_0000.npy')
  # imgs_mask_train = np.load(cm.workingPath.training3DSet_path + 'trainMasks_0000.npy')

  print('_' * 30)
  print('Creating and compiling model...')
  print('_' * 30)


  # model = DenseUNet_3D.get_3d_denseunet()
  # model = LSTM_UNet_3D.time_GRU_unet_1_level()
  model = UNet_3D.get_3d_unet()
  # model = ResNet_3D.get_3d_resnet_34()

  modelname = 'model.png'
  plot_model(model, show_shapes=True, to_file=cm.workingPath.model_path + modelname)
  model.summary()

  # Callbacks:
  filepath = cm.workingPath.model_path + 'weights.{epoch:02d}-{loss:.5f}.hdf5'
  bestfilepath = cm.workingPath.model_path + 'Best_weights.{epoch:02d}-{loss:.5f}.hdf5'

  model_checkpoint = callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=0, save_best_only=False)
  model_best_checkpoint = callbacks.ModelCheckpoint(bestfilepath, monitor='val_loss', verbose=0, save_best_only=True)

  # history = cm.LossHistory_Gerda(cm.workingPath.working_path)
  history = cb.LossHistory()
  # model_history = callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True, write_images=True,
  #  							embeddings_freq=1, embeddings_layer_names=None, embeddings_metadata= None)

  callbacks_list = [history, model_best_checkpoint]

  # Should we load existing weights?
  # Set argument for call to train_and_predict to true at end of script
  if use_existing:
    model.load_weights('./unet.hdf5')

  print('-' * 30)
  print('Fitting model...')
  print('-' * 30)

  model.fit(imgs_train, imgs_mask_train, batch_size=1, epochs=4000, verbose=1, shuffle=True,
            validation_split=0.1, callbacks=callbacks_list)

  print('training finished')


if __name__ == '__main__':
  # Choose whether to train based on the last model:
  # Show runtime:
  starttime = datetime.datetime.now()

  # train_and_predict(True)
  train_and_predict(False)

  endtime = datetime.datetime.now()
  print(endtime - starttime)


  sys.exit(0)