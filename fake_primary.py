from csv import DictWriter
from random import randint


def create_fake_data(movie_name):
    recommend = ['Yes', 'No']
    return {
        "movie_name": movie_name,
        "recommend": recommend[randint(0, 1)],
        "review": "fake data",
        "score": randint(0, 10)
    }


if __name__ == '__main__':
    keys = ['movie_name', 'recommend', 'review', 'score']
    with open('movie_title.csv', encoding='utf-8') as read_file:
        data_list = read_file.readlines()
        with open('review_result.csv', 'w', encoding='utf-8') as my_file:
            writer = DictWriter(my_file, keys)
            for i in range(50):
                for title in data_list:
                    review = create_fake_data(title.strip('\n'))
                    writer.writerow(review)
