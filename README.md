<p>На главной странице сервиса пользователь может выбрать одну или несколько валют.
По нажатию на кнопку “Получить котировку”/“Получить котировки” 
(если выбрано несколько котировок) должна формироваться простая таблица с котировками,
содержащая несколько  столбцов:</p>
<ul>
<li>Код валюты</li>
<li>Название валюты</li>
<li>Цена</li>
<li>Дата котировки</li>
<li>Номинал</li> (например, ЦБ РФ формирует для йены котировки не за 1 единицу, а за 100. Следовательно, номинал будет 100)
</ul>
<p>На странице с таблицей должны быть кнопки/ссылки, позволяющие экспортировать данные
в несколько форматов:
<ul>
<li>CSV</li>
<li>XLSX</li>
<li>PDF</li>
</ul>
<p>Результаты импорта в XLSX и PDF должны иметь приятный читаемый вид,
в идеале верстка должна быть примерно похожа на верстку на фронте</p>


<p>Подготовка места установки на локальном компьютере</p>
<ul>
<li>mkdir taskmanager && cd taskmanager</li>
<li>python -m venv venv</li>
<li>source venv/bin/activate</li>
<li>git clone this repo ...</li>
</ul>
<p>Установка зависимостей проекта</p>
<ul>
<li>Создайте в папке "config" файл ".env"</li>
<li>Добавте в него строку SECRET_KEY="..ваш пароль.."</li>
<li>pip install -r requirements.txt</li>
</ul>
<p>Run the command(local webserver): python manage.py runserver</p>
<p>Смотреть в браузере по адресу http://localhost:8000</p>
