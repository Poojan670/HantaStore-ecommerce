from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


class Categories(models.Model):

    product_choices = (
        ('Automotive Parts & Accessories', 'Automotive Parts & Accessories'),
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Cosmetics', 'Cosmetics'),
        ('Toys & Games', 'Toys & Games'),
        ('Video Games', 'Video Games'),
        ('Tobacco, Pipes & Accessories', 'Tobacco, Pipes & Accessories'),
        ('Other', 'Other'),
    )
    product_category = models.CharField(
        choices=product_choices, null=True, blank=True, max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    featured = models.ImageField(null=True, blank=True, upload_to='products')

    product_category = models.ForeignKey(
        Categories, on_delete=models.CASCADE)
    product_description1 = models.TextField(null=True, blank=True)
    product_description2 = models.TextField(null=True, blank=True)

    avg_rating = models.IntegerField(default=1,
                                     validators=[MinValueValidator(1), MaxValueValidator(5)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.featured.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        sum = 0
        ratings = Rating.objects.filter(product=self)
        total_ratings = len(ratings)
        for rating in ratings:
            sum += rating.stars
        try:
            avg = sum / total_ratings
            self.avg_rating = avg
            super(Product, self).save()
        except:
            self.avg_rating = self.avg_rating
            super(Product, self).save()


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for i in order_items:
            if not i.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images')

    @property
    def ProductimageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=1,
                                validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return str(self.product) + "---" + str(self.user)
