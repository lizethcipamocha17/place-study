# Django Rest Framework
from rest_framework import serializers

# Models
from apps.accounts.api.serializers.users import UserTeacherSerializer
from apps.accounts.models import User
from apps.contents.models import DocumentContent, Content, Like, Comment

from apps.utils.contents import save_document_content, update_document_content


class DocumentContentSerializer(serializers.Serializer):
    """Document Content Serializer"""
    file = serializers.FileField()
    url = serializers.URLField(required=False)
    file_type = serializers.ChoiceField(choices=DocumentContent.FileType.choices)
    file_name = serializers.CharField(required=False)

    class Meta:
        fields = ('file', 'url', 'file_type', 'file_name')


class ContentSerializer(serializers.ModelSerializer):
    """
    ContentSerializer is serializer of content
    """
    author = UserTeacherSerializer(read_only=True)
    documents = DocumentContentSerializer(many=True, required=False)

    class Meta:
        model = Content
        fields = (
            'content_id', 'name', 'description', 'image', 'created_at', 'updated_at',
            'documents', 'author'
        )

    def create(self, validated_data):
        documents = validated_data.pop('documents', None)
        content = Content.objects.create(author=self.context['request'].user, **validated_data)
        save_document_content(documents, content)
        return content

    def update(self, instance, validated_data):
        documents = validated_data.pop('documents', None)
        print(documents, 'documents update')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return update_document_content(documents, instance)


class ContentListSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    author = UserTeacherSerializer(read_only=True)
    documents = DocumentContentSerializer(many=True, read_only=True)
    documents_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Content
        fields = (
            'content_id', 'name', 'description', 'image', 'created_at', 'updated_at', 'likes', 'comment',
            'documents', 'author', 'documents_count'
        )

    def get_likes(self, obj):
        """This function returns all likes by content"""
        return Like.objects.filter(content=obj).count()

    def get_comment(self, obj):
        return Comment.objects.filter(content=obj).count()

    def get_documents_count(self, obj):
        return DocumentContent.objects.filter(content=obj).count()


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


class LikeListUser(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('like_id', 'like', 'content_id', 'user_id')
