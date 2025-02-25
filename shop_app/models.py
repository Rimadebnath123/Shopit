from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    CATEGORY = (
        ("Electronics", "ELECTRONICS"),
        ("Groceries", "GROCERIES"),
        ("Clothings", "CLOTHINGS"),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="img",blank=True)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Check if the slug field is empty
            self.slug = slugify(self.name)  # Generate a slug from the name
            unique_slug = self.slug
            counter = 1
            # Ensure the slug is unique
            if Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{counter}'
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)  # Call the parent class's save method
