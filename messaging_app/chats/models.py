"""
Django models for the messaging and booking application.

This module defines models for:
- CustomUser (extends AbstractUser with custom fields).
- Conversation and Message (messaging system).
- Property, Booking, Payment, Review (hospitality platform).

Constraints and indexing are implemented as required.
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser.

    Fields:
        user_id (UUIDField): Primary key, unique and indexed.
        email (EmailField): Unique, required email for login.
        phone_number (CharField): Optional user phone number.
        role (CharField): Role choices: guest, host, or admin.
        created_at (DateTimeField): Auto timestamp at creation.
        password_hash (CharField): Stores hashed password manually.

    Constraints:
        - Unique constraint on email.
        - Non-null on required fields.
    """

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    email = models.EmailField(unique=True, null=False, db_index=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='guest'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    password_hash = models.CharField(max_length=128, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        """
        Save method override.

        Ensures password_hash is updated whenever the user is saved.
        If using Django's set_password, the password field is hashed
        automatically and copied into password_hash for redundancy.
        """
        if self.password:
            self.password_hash = self.password
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the CustomUser.
        """
        return f"{self.email} ({self.role})"


class Conversation(models.Model):
    """
    Conversation model tracking participants.

    Fields:
        conversation_id (UUIDField): Primary key, unique and indexed.
        participants (ManyToManyField): Links to CustomUser objects.
        created_at (DateTimeField): Auto timestamp at creation.
    """

    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Conversation.
        """
        return (
            f"Conversation {self.conversation_id} with "
            f"{self.participants.count()} participants"
        )


class Message(models.Model):
    """
    Direct message model between two users.

    Fields:
        message_id (UUIDField): Primary key, unique and indexed.
        sender (ForeignKey): User sending the message.
        recipient (ForeignKey): User receiving the message.
        message_body (TextField): The content of the message.
        sent_at (DateTimeField): Auto timestamp when sent.

    Constraints:
        - Foreign key constraints on sender and recipient.
    """

    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )

    message_body = models.TextField(null=False, blank=False)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Message.
        """
        return (
            f"From {self.sender.email} to {self.recipient.email}: "
            f"{self.message_body[:30]}"
        )


class Property(models.Model):
    """
    Property model for listings hosted by users.

    Fields:
        property_id (UUIDField): Primary key, unique and indexed.
        host (ForeignKey): References CustomUser (role = host).
        created_at (DateTimeField): Auto timestamp at creation.

    Constraints:
        - Foreign key constraint on host_id.
        - Non-null on essential attributes.
    """

    property_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Property.
        """
        return f"Property {self.property_id} hosted by {self.host.email}"


class Booking(models.Model):
    """
    Booking model linking users to properties.

    Fields:
        booking_id (UUIDField): Primary key, unique and indexed.
        property (ForeignKey): References Property.
        user (ForeignKey): References CustomUser.
        status (CharField): Booking status.
        created_at (DateTimeField): Auto timestamp at creation.

    Constraints:
        - Foreign key constraints on property_id and user_id.
        - Status must be pending, confirmed, or canceled.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="bookings",
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Booking.
        """
        return f"Booking {self.booking_id} for {self.property}"


class Payment(models.Model):
    """
    Payment model linked to a booking.

    Fields:
        payment_id (UUIDField): Primary key, unique.
        booking (ForeignKey): References Booking.
        created_at (DateTimeField): Auto timestamp at creation.

    Constraints:
        - Foreign key constraint on booking_id.
    """

    payment_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments",
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Payment.
        """
        return f"Payment {self.payment_id} for booking {self.booking}"


class Review(models.Model):
    """
    Review model for properties.

    Fields:
        review_id (UUIDField): Primary key, unique.
        property (ForeignKey): References Property.
        user (ForeignKey): References CustomUser.
        rating (IntegerField): Rating between 1 and 5.
        created_at (DateTimeField): Auto timestamp at creation.

    Constraints:
        - Foreign key constraints on property_id and user_id.
        - Rating must be between 1 and 5.
    """

    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="reviews"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Save method override.

        Ensures rating value is between 1 and 5 before saving.
        """
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Review.
        """
        return f"Review {self.review_id} - {self.rating} stars"
