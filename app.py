from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
# Replace with a secure secret key
app.config['SECRET_KEY'] = 'sheshraman'


# Get the absolute path to the static/data folder
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
DATA_FOLDER = os.path.join(STATIC_FOLDER, 'data')

# Specify the CSV file path within the static/data folder
CSV_FILE_PATH = os.path.join(DATA_FOLDER, 'dump.csv')

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for('admin'))

        flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')




def filter_data(domain):

    # Read CSV file and filter data based on the provided domain
    df = pd.read_csv(CSV_FILE_PATH)

    # Select only the desired columns
    selected_columns = ['Date', 'Name of the Employee', 'LOB', 'Supervisor', 'Part Full', 'Accepted', 'Avg Handle Time', 'Avg Hold Time', 'Active Time',
                        'Ready Time', 'Not Ready Time', 'Busy Time', 'Occupancy', 'FCR Score (Sum)', 'NPS Score (Sum)', 'CSAT Score (Sum)', 'Quality Score']
    filtered_data = df[df['Domain Name'] == domain][selected_columns]

    selected_columns_nonVisible = [
        'Quality Count', 'FCR Count', 'NPS Count', 'CSAT Count']
    filtered_data_nonVisible = df[df['Domain Name']
                                  == domain][selected_columns_nonVisible]

    # select the active column
    Accepted = pd.to_numeric(filtered_data['Accepted'], errors='coerce')
    Total_Accepted = Accepted.sum()

    avg_handle_time = filtered_data['Avg Handle Time'].replace('A', pd.NaT)
    # convert the avg handle time to time delta
    avg_handle_time = pd.to_timedelta(avg_handle_time, errors='coerce')
    # drop rows with NaN values in the Avg Handle Time column
    avg_handle_time = avg_handle_time.mean()
    # Assuming avg_handle_time is a timedelta object
    avg_handle_time = avg_handle_time.total_seconds()
    avg_handle_time = round(avg_handle_time, 2)


    avg_hold_time = filtered_data['Avg Hold Time'].replace('A', pd.NaT)
    avg_hold_time = pd.to_timedelta(avg_hold_time, errors='coerce')
    avg_hold_time = avg_hold_time.mean()
    avg_hold_time = avg_hold_time.total_seconds()
    avg_hold_time = round(avg_hold_time, 2)
   # avg_hold_time = avg_hold_time.days * 24 * 3600 + avg_hold_time.seconds

    active_time = filtered_data['Active Time'].replace('A', pd.NaT)
    active_time = pd.to_timedelta(active_time, errors='coerce')
    total_active_time = active_time.sum()
    total_active_time_formatted = str(total_active_time).split()[-1]
    total_active_time = '{:02}:{:02}:{:02}'.format(
        total_active_time.days * 24 + total_active_time.seconds // 3600,
        (total_active_time.seconds // 60) % 60,
        total_active_time.seconds % 60
    )

    ready_time = filtered_data['Ready Time']
    ready_time = pd.to_timedelta(ready_time, errors='coerce')
    total_ready_time = ready_time.sum()
   # Convert total_ready_time to hh:mm:ss format
    total_ready_time_formatted = str(total_ready_time).split()[-1]
    total_ready_time = '{:02}:{:02}:{:02}'.format(
        total_ready_time.days * 24 + total_ready_time.seconds // 3600,
        (total_ready_time.seconds // 60) % 60,
        total_ready_time.seconds % 60
    )

    not_ready_time = filtered_data['Not Ready Time']
    not_ready_time = pd.to_timedelta(not_ready_time, errors='coerce')
    total_not_ready_time = not_ready_time.sum()
    total_not_ready_time_formatted = str(total_not_ready_time).split()[-1]
    total_not_ready_time = '{:02}:{:02}:{:02}'.format(
        total_not_ready_time.days * 24 + total_not_ready_time.seconds // 3600,
        (total_not_ready_time.seconds // 60) % 60,
        total_not_ready_time.seconds % 60
    )

    busy_time = filtered_data['Busy Time']
    busy_time = pd.to_timedelta(busy_time, errors='coerce')
    total_busy_time = busy_time.sum()
    total_busy_time = '{:02}:{:02}:{:02}'.format(
        total_busy_time.days * 24 + total_busy_time.seconds // 3600,
        (total_busy_time.seconds // 60) % 60,
        total_busy_time.seconds % 60
    )

    occupancy = filtered_data['Occupancy']
    occupancy = pd.to_numeric(occupancy.str.rstrip('%'), errors='coerce')
    average_occupancy = occupancy.mean()
    average_occupancy = round(average_occupancy, 3)

    fcr_score = filtered_data['FCR Score (Sum)']
    fcr_score = pd.to_numeric(fcr_score.str.rstrip('%'), errors='coerce')
    total_fcr_score = fcr_score.sum()
    total_fcr_count = filtered_data_nonVisible['FCR Count']
    total_fcr_count = total_fcr_count.sum()
    Fcr_Score = (total_fcr_score/total_fcr_count)
    Fcr_Score = round(Fcr_Score, 3)

    nps_score = filtered_data['NPS Score (Sum)']
    nps_score = pd.to_numeric(nps_score.str.rstrip('%'), errors='coerce')
    total_nps_score = nps_score.sum()
    total_nps_count = filtered_data_nonVisible['NPS Count']
    total_nps_count = total_nps_count.sum()
    Nps_Score = (total_nps_score/total_nps_count)
    Nps_Score = round(Nps_Score, 3)

    csat_score = filtered_data['CSAT Score (Sum)']
    csat_score = pd.to_numeric(csat_score.str.rstrip('%'), errors='coerce')
    total_csat_score = csat_score.sum()
    total_csat_count = filtered_data_nonVisible['CSAT Count']
    total_csat_count = total_csat_count.sum()
    Csat_Score = (total_csat_score/total_csat_count)
    Csat_Score = round(Csat_Score, 3)

    quality_score = filtered_data['Quality Score']
    quality_score = pd.to_numeric(quality_score.str.rstrip('%'))
    total_quality_score = quality_score.sum()
    total_quality_count = filtered_data_nonVisible['Quality Count']
    total_quality_count = total_quality_count.sum()
    Quality_Score = (total_quality_score/total_quality_count)
    Quality_Score = round(Quality_Score, 3)

    # Create a dictionary to pass value to the HTML template

    result_dict = {
        'Accepted': Total_Accepted,
        'average_handle_time': avg_handle_time,
        'average_hold_time':avg_hold_time,
        'total_active_time': total_active_time,
        'total_ready_time': total_ready_time,
        'total_not_ready_time': total_not_ready_time,
        'total_busy_time': total_busy_time,
        'occupancy': average_occupancy,
        'total_fcr_score': Fcr_Score,
        'total_nps_score': Nps_Score,
        'total_csat_score': Csat_Score,
        'total_quality_score': Quality_Score
    }

    return filtered_data, result_dict


@app.route('/index', methods=['GET', 'POST'])
def index():
    # No need for authentication to access the index page
    if request.method == 'POST':
        domain = request.form['domain']
        filtered_data, result_dict = filter_data(domain)
        return render_template('result.html', data=filtered_data.to_html(index=False), result_dict=result_dict)
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Check if the user is authenticated
    if request.method == 'POST':
        domain = request.form['domain']
        filtered_data, result_dict = filter_data(domain)
        return render_template('result.html', data=filtered_data.to_html(index=False), result_dict=result_dict)
    return render_template('admin.html')


@app.route('/update-csv', methods=['POST'])
def update_csv():
    if 'csv_file' in request.files:
        csv_file = request.files['csv_file']
        new_csv_path = 'C:/Users/sheshraman chaudhary/Desktop/dump.csv'
        csv_file.save(new_csv_path)
        global CSV_FILE_PATH
        CSV_FILE_PATH = new_csv_path
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)
