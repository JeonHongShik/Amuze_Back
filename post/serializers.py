from rest_framework import serializers
from .models import Post, Image, wishtype

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class WishTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = wishtype
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    wish_types = WishTypeSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'region', 'type', 'pay', 'deadline', 'datetime', 'introduce', 'wish_types', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        wish_types_data = validated_data.pop('wish_types')

        post = Post.objects.create(**validated_data)

        for image_data in images_data:
            Image.objects.create(post=post, **image_data)

        for wish_type_data in wish_types_data:
            wishtype.objects.create(post=post, **wish_type_data)

        return post

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.title = validated_data.get('title', instance.title)
        instance.region = validated_data.get('region', instance.region)
        instance.type = validated_data.get('type', instance.type)
        instance.pay = validated_data.get('pay', instance.pay)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.introduce = validated_data.get('introduce', instance.introduce)
        instance.save()

        images = validated_data.get('images')

        if images:
            Image.objects.filter(post=instance).delete()
            for image_data in images:
                Image.objects.create(post=instance, **image_data)

        wish_types = validated_data.get('wish_types')

        if wish_types:
            wishtype.objects.filter(post=instance).delete()
            for wish_type_data in wish_types:
                wishtype.objects.create(post=instance, **wish_type_data)

        return instance
