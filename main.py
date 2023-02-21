# main.py
#   variational auto encoder
# by: Noah Syrkis

# imports
from src import Model, train, load_data, get_args, plot
import torch
from torch import optim, nn
from torch.utils.data import DataLoader


# main
def main():
    # create model
    args = get_args()
    device = "cuda" if torch.cuda.is_available() else 'cpu'
    model = Model(args)
    model.to(device)


    if args.train:
        optimizer = optim.Adam(model.parameters(), lr=args.lr)
        data = load_data()
        loader = DataLoader(data, batch_size=args.batch_size, shuffle=True)
        model = train(model, loader, optimizer, args.epochs, device)
        model = model.to('cpu')
        torch.save(model.state_dict(), f'models/model_dim_{args.latent_dim}.pth')


    if args.generate:
        model.load_state_dict(torch.load(f'models/model_dim_{args.latent_dim}.pth'))
        model.eval()
        z = torch.randn(9 ** 2, args.latent_dim)
        imgs = model.decode(z).reshape(-1, 28, 28).detach().numpy()
        plot(imgs, imgs.shape[0], args)


# run main
if __name__ == '__main__':
    main()

