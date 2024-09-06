import sys
from functools import partial

import numpy as np
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, \
    QColorDialog, QGraphicsRectItem, QSizePolicy
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.patheffects import withStroke

from bar import calculate_all_probabilities
from tool import Ui_Form
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_color = QColor('green')
        # Create the UI using the Ui_Form class
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.colors = ['#ff0000','#0000ff','#00ff00','#f5f5dc']

        self.datas = {
            self.colors[0]: 0,
            self.colors[1]: 0,
            self.colors[2]: 0,
            self.colors[3]: 0,
        }


        button_styleW = '''
            QPushButton {
                border-image: url(wg.png);
                padding: 20px;
                                  margin: 20px;
            }
        '''
        button_styleT = '''
                   QPushButton {
                       border-image: url(tiao.png);
                       padding: 20px;
                                  margin: 20px;
                   }
               '''
        button_styleZ = '''
                      QPushButton {
                          border-image: url(zhe.png);
                          padding: 20px;
                                  margin: 20px;
                      }
                  '''
        button_styleZhu = '''
                              QPushButton {
                                  border-image: url(zhu.png);
                              
                                  padding: 20px;
                                  margin: 20px;
                              }
                          '''
        button_styleB = '''
                              QPushButton {
                                  border-image: url(bing.png);
                                 padding: 20px;
                                  margin: 20px;
                              }
                          '''

        self.ele = self.ui.get_elements()
        self.ele['label'].setPixmap(
            QPixmap('photo.png')
        )
        self.placeholder1 = self.ele['widget']
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.view = self.ele['graphicsView']
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        # Add QGraphicsView to the main window
        layout = self.ele['verticalLayout']
        layout.addWidget(self.view)
        self.scene.addWidget(self.view)
        # Add self.view to self.scene
        self.ele['pushButton_3'].setStyleSheet(button_styleZ)
        self.ele['pushButton_4'].setStyleSheet(button_styleZhu)
        self.ele['pushButton_5'].setStyleSheet(button_styleB)
        self.ele['pushButton_6'].setStyleSheet(button_styleT)
        # self.ele['pushButton'].clicked.connect(self.chooseColorFromPalette)
        self.ele['pushButton_2'].clicked.connect(partial(self.startDrawImg,1))
        self.ele['pushButton_3'].clicked.connect(partial(self.startDrawImg,2))
        self.ele['pushButton_4'].clicked.connect(partial(self.startDrawImg,3))
        self.ele['pushButton_5'].clicked.connect(partial(self.startDrawImg,4))
        self.ele['pushButton_6'].clicked.connect(partial(self.startDrawImg,5))
        self.setFixedSize(self.size())
    def draw_grid_chart(self, raw, clos, color_count):
        # Grid chart data
        self.scene.clear()

        # Use the number of rows and columns passed
        num_rows = raw
        num_cols = clos
        # Calculate the width and height of the cell
        cell_width = 550 // num_cols
        cell_height = 400 // num_rows
        # Draw a grid
        for row_index in range(num_rows):
            for col_index in range(num_cols):
                color = next(iter(color_count))  # Get the next color
                print(color)
                count = color_count[color]

                rect_item = QGraphicsRectItem(col_index * cell_width, row_index * cell_height, cell_width, cell_height)
                rect_item.setBrush(QColor(color))
                self.scene.addItem(rect_item)

                # Reduce the number of colors, if the number is 0, remove the color
                color_count[color] -= 1
                if color_count[color] == 0:
                    del color_count[color]

                if not color_count:  # If the number of colors is empty, exit the loop
                    break

    # Assumed crowd size
    population_size = 1000

    # Define a probability calculation function
    def calculate_all_probabilities(prior_prob, true_positive_rate, false_positive_rate):
        p_positive = (true_positive_rate * prior_prob) + (false_positive_rate * (1 - prior_prob))
        posterior_positive = (true_positive_rate * prior_prob) / p_positive
        p_negative = 1 - p_positive
        true_negative_rate = 1 - false_positive_rate
        posterior_negative = ((1 - true_positive_rate) * prior_prob) / p_negative
        posterior_healthy_negative = true_negative_rate * (1 - prior_prob) / p_negative
        return posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative

    def calculate_gender_specific_probabilities(prior_prob, true_positive_rate, false_positive_rate, male_ratio):
        female_ratio = 1 - male_ratio
        posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative = calculate_all_probabilities(
            prior_prob, true_positive_rate, false_positive_rate)
        male_posterior_positive = posterior_positive * male_ratio
        female_posterior_positive = posterior_positive * female_ratio
        return male_posterior_positive, female_posterior_positive


    prior_prob = 0.02
    true_positive_rate = 0.8
    false_positive_rate = 0.1


    posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative = calculate_all_probabilities(
        prior_prob, true_positive_rate, false_positive_rate)

    male_ratio = 0.6
    male_posterior_positive, female_posterior_positive = calculate_gender_specific_probabilities(
        prior_prob, true_positive_rate, false_positive_rate, male_ratio)


    expected_counts_positive_test = np.array([posterior_positive, 1 - posterior_positive]) * population_size
    expected_counts_test_result = np.array([p_positive, p_negative]) * population_size
    expected_counts_negative_test = np.array([posterior_negative, posterior_healthy_negative]) * population_size
    expected_counts_gender_specific = np.array([male_posterior_positive, female_posterior_positive]) * population_size

    # Redraw the histogram
    data = [expected_counts_positive_test, expected_counts_test_result, expected_counts_negative_test,
            expected_counts_gender_specific]
    labels = ['Posterior Probability\nGiven Positive Test', 'Overall Test Result Probability',
              'Posterior Probability\nGiven Negative Test',
              'Gender Specific Posterior Probability\nGiven Positive Test']
    x_ticks_labels = ['P(D+|T+)', 'P(D-|T+)', 'P(T+)', 'P(T-)', 'P(D+|T-)', 'P(D-|T-)', 'Male', 'Female']


    def draw_bar_chart(self, prior_prob, true_positive_rate, false_positive_rate, male_ratio,categories):
        print("Histogram data")
        print(prior_prob,true_positive_rate,false_positive_rate)
        posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative = self.calculate_all_probabilities(
            prior_prob, true_positive_rate, false_positive_rate)
        male_posterior_positive, female_posterior_positive = self.calculate_gender_specific_probabilities(prior_prob,
                                                                                                         true_positive_rate,
                                                                                                          false_positive_rate,
                                                                                                          male_ratio)
        sizes1 = [posterior_positive, 1 - posterior_positive]
        sizes2 = [p_positive, p_negative]
        sizes3 = [posterior_negative, posterior_healthy_negative]
        sizes_gender_specific = [male_posterior_positive, female_posterior_positive]

        labels1 = ['P(D+|T+)', 'P(D-|T+)']
        labels2 = ['P(T+)', 'P(T-)']
        labels3 = ['P(D+|T-)', 'P(D-|T-)']
        labels_gender_specific = ['Male P(D+|T+)', 'Female P(D+|T+)']

        colors1 = ['lightcoral', 'lightskyblue']
        colors2 = ['gold', 'lightgreen']
        colors3 = ['lightpink', 'lightblue']
        colors_gender_specific = ['blue', 'pink']

        explode = (0.1, 0)
        population_size = 1000
        # Clear the previous graphics and reset the canvas
        if self.scene:
            self.scene.clear()
        self.figure, self.ax = plt.subplots(1, 3, figsize=(16, 4))  # 更新为1行4列布局

        # Calculate the expected number of people
        expected_counts_positive_test = np.array([posterior_positive, 1 - posterior_positive]) * population_size
        expected_counts_test_result = np.array([p_positive, p_negative]) * population_size
        expected_counts_negative_test = np.array([posterior_negative, posterior_healthy_negative]) * population_size
        expected_counts_gender_specific = np.array(
            [male_posterior_positive, female_posterior_positive]) * population_size

        # Redraw the histogram
        self.data = [expected_counts_positive_test, expected_counts_test_result, expected_counts_negative_test,
                expected_counts_gender_specific]
        labels = ['Posterior Probability\nGiven Positive Test', 'Overall Test Result Probability',
                  'Posterior Probability\nGiven Negative Test',
                  'Gender Specific Posterior Probability\nGiven Positive Test']
        self.x_ticks_labels = [categories[0], categories[1], categories[2], categories[3], categories[4], categories[5], 'Male', 'Female']

        # Draw a histogram
        self.canvas = FigureCanvas(self.figure)

        for i, ax in enumerate(self.ax.flat):
            ax.bar(self.x_ticks_labels[i * 2:i * 2 + 2], self.data[i], color=['red', 'green'] if i < 3 else ['blue', 'pink'])
            ax.set_title(self.labels[i])
            ax.set_xticklabels(self.x_ticks_labels[i * 2:i * 2 + 2], rotation=45)
            ax.set_ylabel('Expected Count')
        if self.scene:
            self.scene.addWidget(self.canvas)
            if self.view:
                self.view.setScene(self.scene)

        self.canvas.draw()

    def draw_rose_chart(self, prior_prob, true_positive_rate, false_positive_rate, male_ratio,categories):
        print(categories)
        posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative = self.calculate_all_probabilities(
            prior_prob, true_positive_rate, false_positive_rate)
        male_posterior_positive, female_posterior_positive = self.calculate_gender_specific_probabilities(prior_prob,
                                                                                                          true_positive_rate,
                                                                                                          false_positive_rate,
                                                                                                          male_ratio)

        sizes1 = [posterior_positive, 1 - posterior_positive]
        sizes2 = [p_positive, p_negative]
        sizes3 = [posterior_negative, posterior_healthy_negative]
        sizes_gender_specific = [male_posterior_positive, female_posterior_positive]

        # Gets the label from the categories parameter
        labels1 = [categories[0], categories[1]]
        labels2 = [categories[2], categories[3]]
        labels3 = [categories[4], categories[5]]
        labels_gender_specific = ['Male P(D+|T+)', 'Female P(D+|T+)']

        colors1 = ['lightcoral', 'lightskyblue']
        colors2 = ['gold', 'lightgreen']
        colors3 = ['lightpink', 'lightblue']
        colors_gender_specific = ['blue', 'pink']

        explode = (0.1, 0)

        # Clear the previous graphics and reset the canvas
        if self.scene:
            self.scene.clear()
        self.figure, self.ax = plt.subplots(1, 3, figsize=(16, 4))  # 更新为1行4列布局

        self.canvas = FigureCanvas(self.figure)

        self.ax[0].pie(sizes1, explode=explode, labels=labels1, colors=colors1, autopct='%1.1f%%', shadow=True,
                       startangle=140)
        self.ax[1].pie(sizes2, explode=explode, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True,
                       startangle=140)
        self.ax[2].pie(sizes3, explode=explode, labels=labels3, colors=colors3, autopct='%1.1f%%', shadow=True,
                       startangle=140)



        self.ax[0].set_title('Posterior Probability Given Positive Test')
        self.ax[1].set_title('Overall Test Result Probability')
        self.ax[2].set_title('Posterior Probability Given Negative Test')
        # self.ax[3].set_title('Gender-Specific Posterior Probability')

        plt.axis('equal')

        if self.scene:
            self.scene.addWidget(self.canvas)
            if self.view:
                self.view.setScene(self.scene)

        self.canvas.draw()
    def draw_horizontal_bar_chart(self,categories, values,):
        # Clear scene
        self.scene.clear()

        self.placeholder1 = self.ele['widget']
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.canvas.setMinimumSize(550, 400)
        self.canvas.setMaximumSize(550, 400)
        self.view = self.ele['graphicsView']
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)


        layout = self.ele['verticalLayout']
        layout.addWidget(self.view)
        self.scene.addWidget(self.view)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)


        self.ax.barh(categories, values, color=self.colors,height=0.4 )


        self.ax.set_title(' Bayesian')
        self.ax.set_xlabel('num')
        self.ax.set_ylabel('item')


        self.canvas.draw()
    def draw_line_chart(self, categories, values):
        self.scene.clear()

        self.placeholder1 = self.ele['widget']
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.canvas.setMinimumSize(550, 400)
        self.canvas.setMaximumSize(550, 400)
        self.view = self.ele['graphicsView']
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        layout = self.ele['verticalLayout']
        layout.addWidget(self.view)
        self.scene.addWidget(self.view)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.plot(categories, values, marker='o',   markersize=10,  color='skyblue')


        self.ax.set_title(' Bayesian')
        self.ax.set_xlabel('item')
        self.ax.set_ylabel('num')


        self.canvas.draw()

    def calculate_all_probabilities(self, prior_prob, true_positive_rate, false_positive_rate):
        p_positive = (true_positive_rate * prior_prob) + (false_positive_rate * (1 - prior_prob))
        posterior_positive = (true_positive_rate * prior_prob) / p_positive
        p_negative = 1 - p_positive
        true_negative_rate = 1 - false_positive_rate
        # posterior_negative = (false_positive_rate * (1 - prior_prob)) / p_negative
        posterior_negative = ((1 - true_positive_rate) * prior_prob) / p_negative

        posterior_healthy_negative = true_negative_rate * (1 - prior_prob) / p_negative
        return posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative

    def calculate_gender_specific_probabilities(self, prior_prob, true_positive_rate, false_positive_rate, male_ratio):
        female_ratio = 1 - male_ratio
        posterior_positive, _, _, _, _ = self.calculate_all_probabilities(prior_prob, true_positive_rate,
                                                                          false_positive_rate)
        male_posterior_positive = posterior_positive * male_ratio
        female_posterior_positive = posterior_positive * female_ratio
        return male_posterior_positive, female_posterior_positive



    def chooseColorFromPalette(self):
        for i in range(len(self.colors)):
            color = QColorDialog.getColor()
            if color.isValid():
                if color.name() in self.colors:
                    continue
                self.colors[i] = color.name()
        print(self.colors)


