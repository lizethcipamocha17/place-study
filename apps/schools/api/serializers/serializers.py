from rest_framework import serializers
from apps.accounts.models import User
from apps.schools.models import School, Content, Comment, Like


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class UserListRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class CommentCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    text = serializers.CharField(min_length=10, max_length=100, required=True)

    def save(self, **kwargs):
        comment, created = Comment.objects.get_or_create(
            user=self.validated_data['user'], content=self.context['content'], text=self.validated_data['text']
        )

        # mirar si el pk content existe
        # if self.context['content']

        if not created:
            raise serializers.ValidationError('solo puedes comentar una vez por publicación.')
        return comment


class CommentListSerializer(serializers.ModelSerializer):
    user = UserListRelatedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('text', 'content', 'user')


class LikeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('content', 'like',)

    def create(self, data):
        like, created = Like.objects.get_or_create(content_id=self.data['content'], user=self.instance)

        if not created:
            like.delete()

        return self.context['content'], like


class LikeListSerializer(serializers.ModelSerializer):
    user = UserListRelatedSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('content', 'like', 'user')

    def get_total_likes(self, instance):
        return instance.liked_by.all().count()
