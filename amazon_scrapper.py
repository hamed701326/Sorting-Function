import requests
from bs4 import BeautifulSoup

def scrape_amazon_reviews(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Cookie": 'regStatus=pre-register; aws-target-data=%7B%22support%22%3A%221%22%7D; session-id=132-7213693-1491245; i18n-prefs=USD; sp-cdn="L5Z9:IR"; skin=noskin; ubid-main=132-7429225-5164620; lc-main=en_US; session-id-time=2082787201l; session-token=vd67XOSlJEB07EJMtjlqPi89s0RHfaYaMqLRnud/GPrk+CSW6bvtX0TCCPPCgdu6r1yqpfku+MEPNH7MfRAEyuv7FnHyW/HPr0YFYyRDdMw5uaX22wvshKaDnm4ObuYgnYEJvBOC/SrpW1QHgx0M1ydbqORpUHaClEy9eq46BJTmSaPMt7KRvp/ha4u56NeCmOgymYI+ZiTXdl5ggZPcudlqTYqm5W5jfXwXeB9NAPQBbR8ADVTwqch8FKrioTo7lmlPqPWmX/gw8ZxIuS0YzXZdysO02k3QWp8Jwo2rUZEqpdrO7VItq7n25nKFixQzxJU6qvhclcW3ZfOIWjLtNvaedUan4Its'
    }

    reviews = []

    page_number = 1
    while True:
        page_url = f"{url}&reviewerType=all_reviews&pageNumber={page_number}"
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        review_elements = soup.find_all('div', class_='a-section review aok-relative')
        print(review_elements.__sizeof__)
        if not review_elements:
            break  # No more reviews to scrape

        for review in review_elements:
            review_data = {
                'rating': review.find('i', class_='a-icon a-icon-star a-star-5 review-rating').select('span')[0].text,
                'title': review.find('a', class_='review-title').select('span')[2].text,
                'body': review.find('span', class_='review-text').text.strip()
            }
            reviews.append(review_data)

        page_number += 1

    return reviews

