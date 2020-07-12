from datetime import datetime

def logger(oldfoo):
    date = datetime.now()

    def newfoo(*args, **kwargs):
        result = oldfoo(*args, **kwargs)
        with open('logs/decorator_trace.log', 'a', encoding='utf-8') as fi:
            fi.write(f'Вызвали функцию с именем "{oldfoo.__name__}"\n'
                  f'c аргументами "{args}" и "{kwargs}"\n'
                  f'Время старта: {date}\n'
                  f'Возвращаемое значение: "{result}"\n'
                    f'________________________________\n')
            return result