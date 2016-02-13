from database import db_session
from models.Model import User, Result
from sqlalchemy import func
import StringIO
import random
import datetime
import collections

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from flask import request, jsonify, make_response

wake_up_db = db_session.execute("select 1") #Git comment

def register_user(user):
    db_session.add(user)
    db_session.flush()
    return user


def get_user_by_id(input_id):
    user = User.query.filter_by(id=input_id).first()
    number_of_drinks = db_session.query(func.max(Result.number_of_drinks)).filter(Result.user_id == user.id).scalar()
    if user is not None:
        return_user = user.get_object_with_results()
        return_user.update({'number_of_drinks': number_of_drinks})
        return jsonify(user=return_user)
    else:
        return jsonify(user=None)


def get_user_by_name(input_name):
    user = User.query.filter_by(name=input_name).first()
    if user is not None:
        number_of_drinks = db_session.query(func.max(Result.number_of_drinks)).filter(Result.user_id == user.id).scalar()
        return_user = user.get_object_with_results()
        return_user.update({'number_of_drinks': number_of_drinks})
        return jsonify(user=return_user)
    else:
        return jsonify(user=None)


def register_result(result):
    db_session.add(result)
    db_session.flush()
    return result


def get_result_by_id(input_id):
    result = Result.query.filter_by(id=input_id).first()
    if result is not None:
        return jsonify(result=result.get_object())
    else:
        return jsonify(result=None)


def get_result_by_user_name(input_name):
    user = User.query.filter_by(name=input_name).first()
    if user is not None:
        return jsonify(results=user.get_results())
    else:
        return jsonify(result=None)


def get_result_by_user_id(input_id):
    user = User.query.filter_by(id=input_id).first()
    if user is not None:
        return jsonify(results=user.get_results())
    else:
        return jsonify(result=None)


def get_result_by_sex(input_sex):
    user = User.query.filter_by(sex=input_sex).first()
    if user is not None:
        return jsonify(results=user.get_results())
    else:
        return jsonify(result=None)


def get_result_by_age(input_age):
    user = User.query.filter_by(age=input_age).first()
    if user is not None:
        return jsonify(results=user.get_results())
    else:
        return jsonify(result=None)


def get_image_by_user_name(input_name):
    users = User.query.filter_by(name=input_name)
    return structure_plot_data(users)


def get_image_by_sex(input_sex):
    users = User.query.filter_by(sex=input_sex)
    return structure_plot_data(users)

def get_image_by_age(input_age_from, input_age_to):
    users = User.query.filter(User.age >= input_age_from, User.age <= input_age_to)
    print users
    return structure_plot_data(users)


def structure_plot_data(users):
    plot_data = {}
    for i in range(0, 21):
        plot_data[i] = {'reaction_time': 0.0,
                        'distance_from_centre': 0.0,
                        'number_of_rows': 0.0}
    if users is not None:
        for user in users:
            results = user.get_results()
            for result in results:
                data = plot_data[result['number_of_drinks']]

                number_of_rows = data['number_of_rows'] + 1.0
                reaction_time = (data['reaction_time'] + result['reaction_time']) / number_of_rows
                distance_from_centre = (data['distance_from_centre'] + result['distance_from_centre']) / number_of_rows

                plot_data[result['number_of_drinks']] = {'reaction_time': reaction_time,
                                                         'distance_from_centre': distance_from_centre,
                                                         'number_of_rows': number_of_rows}

        ordered_plot_data = collections.OrderedDict(sorted(plot_data.items()))
        return plot_line_chart(ordered_plot_data, "Number of drinks", "Reaction time", "Distance from centre")

    else:
        return jsonify(result=None)


def plotChart(x, y):
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y)
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


def plot_line_chart(data, xlabel, y1label, y2label):
    x = data.keys()
    y1 = []
    y2 = []
    for key, value in data.iteritems():
        y1.append(value['reaction_time'])
        y2.append(value['distance_from_centre'])

    fig, ax = plt.subplots()

    n_groups = len(x)

    means_men = (20, 35, 30, 35, 27)
    #std_men = (2, 3, 4, 1, 2)

    means_women = (25, 32, 34, 20, 25)
    #std_women = (3, 5, 2, 3, 3)

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4

    #rects1 = ax.bar(index, y1, bar_width,
                 #alpha=opacity,
                 #color='b',
                 #yerr=std_men,
                 #error_kw=error_config,
                 #label=y1label)

    #rects2 = ax.bar(index + bar_width, y2, bar_width,
                     #alpha=opacity,
                     #color='r',
                     #yerr=std_women,
                     #error_kw=error_config,
                     #label=y2label)

    ax.plot(x, y1, color='g', label=y1label)
    ax.plot(x, y2, color='r', label=y2label)

    plt.xlabel('Number of drinks')
    plt.ylabel('Scores')
    #plt.title('Scores by group and gender')
    #plt.xticks(index + bar_width, x)
    #ax.set_label_coords(index+bar_width,index)
    plt.legend()
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

