import re


def paremetrized(string):
    def decorator(func):
        def wrapper(*args, **kwargs):
            string_f = string
            if kwargs:
                string_f = string_f.format(**kwargs)
            if args:
                string_f = re.sub(r"{.+}", "{}", string_f).format(*args)
            print(string_f)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@paremetrized("Hi, {name}!")
def hello(name):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    hello("Volodya")
