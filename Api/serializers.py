from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    author = serializers.CharField(required=False)
    likes = serializers.IntegerField(required=False)
    image = serializers.CharField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField(required=False)

    def validate_image(self, value):
        if value and isinstance(value, str):
            if value.startswith('data:image'):
                # Remove data:image/xxx;base64, prefix if present
                if ',' in value:
                    value = value.split(',')[1]
            return value
        return value

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    email = serializers.EmailField()
    profile_picture = serializers.CharField(required=False, allow_blank=True, allow_null=True) 