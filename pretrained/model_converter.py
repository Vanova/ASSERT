"""
https://www.dlology.com/blog/how-to-load-python-2-pytorch-checkpoint-in-python-3-1/

NOTE: run this code in Python 2 & Pytorch<0.4

In Python 3 & Pytorch>0.4 load a `state_dict`:
  state_dict = torch.load(file_state)
  model.load_state_dict(state_dict)
"""

# for saving state only
# model_files = ['pa/senet34', 'la/senet34']
#
# for mf in model_files:
#     path, name = os.path.split(mf)
#     out_file = '%s/%s_py3_state_dict' % (path, name)
#     checkpoint = torch.load(mf, map_location=lambda storage, loc: storage)
#     # save the `state_dict` object
#     torch.save(checkpoint['state_dict'], out_file)
#     print('Model is converted: %s --> %s' % (mf, out_file))

# Do this from Python 2.X and pytorch 0.4.0
import os
import torch
import pickle

model_files = ['pa/senet34', 'la/senet34']

py2 = False
py3 = True

if py2:
    for mf in model_files:
        checkpoint = torch.load(mf, map_location=lambda storage, loc: storage)
        # save the checkpoint
        path, name = os.path.split(mf)
        out_file = '%s/%s_py2.pkl' % (path, name)
        with open(out_file, "wb") as outfile:
            pickle.dump(checkpoint, outfile)
        print('Model checkpoint is saved: %s --> %s' % (mf, out_file))

if py3:
    for mf in model_files:
        # Load the pickle file in Python 3.X
        with open(mf + '_py2.pkl', 'rb') as f:
            data_dict = pickle.load(f, encoding='bytes')

        # View the keys, this prints bytes.
        print(data_dict.keys())

        # Turn OrderedDict to normal dict.
        data_dict = dict(data_dict)

        # Convert the first level keys.
        data_dict = dict((key.decode(), value) for (key, value) in data_dict.items())

        # This should print strings
        print(data_dict.keys())

        # Convert the second level 'state_dict' keys.
        data_dict['state_dict'] = dict(data_dict['state_dict'])
        data_dict['state_dict'] = dict((key.decode(), value) for (key, value) in data_dict['state_dict'].items())

        # This should print strings
        print(data_dict['state_dict'].keys())

        path, name = os.path.split(mf)
        torch.save(data_dict, "{}/{}_py3".format(path, 'senet34'))

        # It should have no issue.
        checkpoint = torch.load("{}/{}_py3".format(path, 'senet34'))
