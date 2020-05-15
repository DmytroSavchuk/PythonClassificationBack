import uuid

import matplotlib.pyplot as plt
from pandas import np

from Classification_Project.ApplicationConstants import ApplicationConstants
from Classification_Project.FileUtils import file_utils


class Plotter:
    def build_histogram(self, method_params, y_param_name, title, x_label=None, y_label=None, descending=False):
        self.__config_plot()

        x = []
        y = []

        method_names = list(method_params.keys())
        method_names.sort(reverse=descending, key=lambda m: getattr(method_params[m], y_param_name))

        for method in method_names:
            x.append(method)
            y.append(getattr(method_params[method], y_param_name))

        plt.bar(np.array(self.__prepare_method_labeles(x)), np.array(y), width=0.5)

        self.draw_bar_labels(y, len(x))

        plt.title(title)
        if x_label is not None:
            plt.xlabel(x_label)
        if y_label is not None:
            plt.ylabel(y_label)

        result = self.__read_plot_as_stream(plt)

        plt.close()

        return result

    def draw_bar_labels(self, y, x_length):
        y_max = max(y)

        for i in range(x_length):
            plt.text(x=i, y=y[i] + y_max / 100, s='%.5f' % y[i], size=10, horizontalalignment='center')

    def __config_plot(self):
        font = {'weight': 'regular',
                'size': 15}

        plt.rc('font', **font)

        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)

        plt.locator_params(axis='y', nbins=10)

    def __read_plot_as_stream(self, plt):
        plot_path = f'{ApplicationConstants.get_constant("UPLOADS_FOLDER_PATH")}/{uuid.uuid1()}.png'

        plt.savefig(plot_path)

        return file_utils.read_file(plot_path, True)

    def __prepare_method_labeles(self, method_names):
        labels = []

        for name in method_names:
            if 'Classifier' in name:
                labels.append(name[:name.index('Classifier')] + '\n' + name[name.index('Classifier'):])
            elif 'Regression' in name:
                labels.append(name[:name.index('Regression')] + '\n' + name[name.index('Regression'):])
            else:
                labels.append(name)

        return labels


plotter = Plotter()
