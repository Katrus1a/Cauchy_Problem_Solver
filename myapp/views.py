import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, lambdify, symbols, sqrt, cos, sin, tan, cot, Abs
from django.shortcuts import render
import io
import urllib, base64
from .forms import UserInputForm


def euler_method(f, x0, y0, h, x_end):
    n = int((x_end - x0) / h)
    x_vals = [x0]
    y_vals = [y0]
    for i in range(n):
        try:
            y_next = y_vals[-1] + h * f(x_vals[-1], y_vals[-1])
            # Перетворіть значення на float перед перевіркою
            y_next = float(y_next)
            if np.isnan(y_next) or np.isinf(y_next):
                raise ValueError("Calculation resulted in an invalid value (NaN or Inf).")
            x_vals.append(x_vals[-1] + h)
            y_vals.append(y_next)
        except ZeroDivisionError:
            print(f"Zero division error at step {i} (x={x_vals[-1]:.4f}, y={y_vals[-1]:.4f}). Skipping this step.")
            break
        except ValueError as e:
            print(f"Error at step {i} (x={x_vals[-1]:.4f}, y={y_vals[-1]:.4f}): {e}")
            break
    return x_vals, y_vals


def euler_cauchy_method(f, x0, y0, h, x_end):
    n = int((x_end - x0) / h)
    x_vals = [x0]
    y_vals = [y0]
    for i in range(n):
        try:
            y_tilde = y_vals[-1] + h * f(x_vals[-1], y_vals[-1])
            # Перетворіть значення на float перед перевіркою
            y_tilde = float(y_tilde)
            if np.isnan(y_tilde) or np.isinf(y_tilde):
                raise ValueError("Calculation resulted in an invalid value (NaN or Inf).")
            y_next = y_vals[-1] + h / 2 * (f(x_vals[-1], y_vals[-1]) + f(x_vals[-1] + h, y_tilde))
            # Перетворіть значення на float перед перевіркою
            y_next = float(y_next)
            if np.isnan(y_next) or np.isinf(y_next):
                raise ValueError("Calculation resulted in an invalid value (NaN or Inf).")
            x_vals.append(x_vals[-1] + h)
            y_vals.append(y_next)
        except ZeroDivisionError:
            print(f"Zero division error at step {i} (x={x_vals[-1]:.4f}, y={y_vals[-1]:.4f}). Skipping this step.")
            break
        except ValueError as e:
            print(f"Error at step {i} (x={x_vals[-1]:.4f}, y={y_vals[-1]:.4f}): {e}")
            break
    return x_vals, y_vals


def home(request):
    return render(request, 'myapp/home.html')


def main_view(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            equation = form.cleaned_data['equation']
            x0 = form.cleaned_data['x0']
            y0 = form.cleaned_data['y0']
            x_end = form.cleaned_data['x_end']
            h = form.cleaned_data['h']
            method = form.cleaned_data['method']

            try:
                # Символи для використання у функції
                x, y = symbols('x y')

                # Спроба створення виразу на основі введеного рівняння
                f_expr = sympify(equation,
                                 locals={'sqrt': sqrt, 'cos': cos, 'sin': sin, 'tan': tan, 'cot': cot, 'abs': Abs})

                # Створюємо функцію на основі виразу
                f = lambdify((x, y), f_expr, modules=['numpy'])

                if method == 'euler':
                    x_vals, y_vals = euler_method(f, x0, y0, h, x_end)
                    title = "Euler Method"
                elif method == 'euler-cauchy':
                    x_vals, y_vals = euler_cauchy_method(f, x0, y0, h, x_end)
                    title = "Euler-Cauchy Method"
                else:
                    return render(request, 'myapp/main.html', {'form': form, 'error': 'Invalid method selected.'})

                # Побудова графіка
                fig, ax = plt.subplots()
                ax.plot(x_vals, y_vals, marker='o')
                ax.set_title(title)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.grid(True)

                # Збереження графіка як зображення
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                string = base64.b64encode(buf.read())
                uri = urllib.parse.quote(string)

                table_data = zip(range(len(x_vals)), x_vals, y_vals)

                return render(request, 'myapp/main.html', {
                    'form': form,
                    'plot': uri,
                    'table_data': table_data,
                    'title': title
                })

            except Exception as e:
                return render(request, 'myapp/main.html', {'form': form, 'error': str(e)})
    else:
        form = UserInputForm()

    return render(request, 'myapp/main.html', {'form': form})
