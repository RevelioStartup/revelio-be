from rest_framework import serializers
from .models import Profile
from django.core.files.storage import default_storage

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']  # Add other fields as needed

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)

        if 'profile_picture' in validated_data:
            # Check if the instance already has a profile picture
            if instance.profile_picture:
                # If so, delete the old file from storage
                old_file = instance.profile_picture
                if default_storage.exists(old_file.name):
                    default_storage.delete(old_file.name)

            # Now set the new profile picture
            instance.profile_picture = validated_data.get('profile_picture')

        instance.save()
        return instance
