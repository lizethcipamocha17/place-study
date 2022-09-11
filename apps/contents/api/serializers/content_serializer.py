# Django Rest Framework
from rest_framework import serializers

# Models
from apps.accounts.api.serializers.users import UserTeacherSerializer
from apps.accounts.models import User
from apps.contents.models import DocumentContent, Content, Like, Comment

from apps.utils.schools import save_document_content


class DocumentContentSerializer(serializers.ModelSerializer):
    """Document Content Serializer"""

    file_name = serializers.SerializerMethodField()
    # file_url = serializers.SerializerMethodField()

    class Meta:
        model = DocumentContent
        exclude = ('content',)

    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1]

    # def get_file_url(self, obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.file.url)


class ContentSerializer(serializers.ModelSerializer):
    """
    ContentSerializer is serializer of content
    """
    likes = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    author = UserTeacherSerializer(read_only=True)
    documents = DocumentContentSerializer(many=True, required=False)

    class Meta:
        model = Content
        fields = (
            'content_id', 'name', 'description', 'image', 'created_at', 'updated_at', 'likes', 'comment',
            'documents', 'author'
        )

    def create(self, validated_data):
        documents = validated_data.pop('documents', None)
        content = Content.objects.create(author=self.context['author'], **validated_data)
        save_document_content(documents, content)
        return content

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
