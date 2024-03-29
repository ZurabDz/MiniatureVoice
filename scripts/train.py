from miniature_voice.datamodule import CommonVoiceDataModule
from miniature_voice.model import MiniatureVoice
import pytorch_lightning as pl
from pytorch_lightning.strategies import DeepSpeedStrategy
# import composer.functional as cf
from argparse import ArgumentParser

 
parser = ArgumentParser(
    prog="Train Miniature Voice",
    description="configurtion miniature voice and training it",
)

parser.add_argument('--root_data', help="common voice dataset root dir", required=True)
parser.add_argument('--batch_size', required=True, type=int)
parser.add_argument('--max_epochs', required=True, type=int)
parser.add_argument('--check_val_every_n_epochs', required=True, type=int)
parser.add_argument('--accumulate_grad_batches', required=True, type=int)
parser.add_argument('--num_heads', required=True, type=int)
parser.add_argument('--ffn_dim', required=True, type=int)
parser.add_argument('--num_layers', required=True, type=int)
parser.add_argument('--precision', type=int)


args = parser.parse_args()

model = MiniatureVoice(num_heads=args.num_heads, ffn_dim=args.ffn_dim, num_layers=args.num_layers, input_dim=80)


data_module = CommonVoiceDataModule(args.root_data, batch_size=args.batch_size)

trainer = pl.Trainer(accelerator='gpu', gradient_clip_val=1, max_epochs=args.max_epochs,
                     precision=args.precision, check_val_every_n_epoch=args.check_val_every_n_epochs,
                     accumulate_grad_batches=args.accumulate_grad_batches,
                     # strategy='deepspeed'
                     # strategy=DeepSpeedStrategy(
                     #         stage=3,
                     #         offload_optimizer=True,
                     #         offload_parameters=True,
                     #     ),
                     )
trainer.fit(model, datamodule=data_module)
