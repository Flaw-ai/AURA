import torch

def count_parameters(model):
    return sum(
        p.numel()
        for p in model.parameters()
    )

def count_trainable_parameters(model):
    return sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )


def model_size_mb(model):
    params = count_parameters(model)
    return (params * 4) / (1024 ** 2)


def freeze_model(model):
    for param in model.parameters():
        param.requires_grad = False

    return model


def unfreeze_model(model):
    for param in model.parameters():
        param.requires_grad = True

    return model


def move_to_device(model, device):
    return model.to(device)


def get_device():
    if torch.cuda.is_available():
        return "cuda"

    return "cpu"