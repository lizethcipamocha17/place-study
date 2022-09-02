# Django Rest Framework
from rest_framework import serializers

# Models
from apps.accounts.models import User
from apps.schools.models import School, Content, Comment, Like


class SchoolSerializer(serializers.ModelSerializer):
    """
    SchoolSerializer is serializer of school
    """

    class Meta:
        model = School
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    """
    ContentSerializer is serializer of content
    """
    likes = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = Content
        fields = '__all__'


    def create(self, validated_data):
        return Content.objects.create(school=self.context['school'], **validated_data)

    def get_likes(self, obj):
        """This function returns all likes by content"""
        return Like.objects.filter(content=obj).count()

    def get_comment(self, obj):
        return Comment.objects.filter(content=obj).count()


class UserListRelatedSerializer(serializers.ModelSerializer):
    """
    UserListRelatedSerializer is serializer of  user list related
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class CommentCreateSerializer(serializers.Serializer):
    """
    CommentCreateSerializer is serializer of  comment create
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    text = serializers.CharField(min_length=10, max_length=100, required=True)

    def save(self, **kwargs):
        """This function save the comments """
        comment, created = Comment.objects.get_or_create(
            user=self.validated_data['user'], content=self.context['content'], text=self.validated_data['text']
        )

        if not created:
            raise serializers.ValidationError('solo puedes comentar una vez por publicación.')
        return comment


class CommentListSerializer(serializers.ModelSerializer):
    """
    CommentListSerializeris the serializer of the comment list
    """
    user = UserListRelatedSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('text', 'content', 'user')


class LikeCreateSerializer(serializers.Serializer):
    """
    LikeCreateSerializer is serializer of like create
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, data):
        """This function creates like by content"""
        content = self.context['content']
        user = self.validated_data['user']

        like, created = Like.objects.get_or_create(content=content, user=user, like=True)
        return like
