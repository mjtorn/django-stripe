# Third Party Stuff
from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string


class AbstractStripeModelAdmin(admin.ModelAdmin):
    stripe_model_action = None
    actions = ["sync_all"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_action_buttons(self):
        """
        Return a list of button configurations. Each button has a 'label' and 'url'.
        """
        return [
            {"label": "Sync all from stripe", "url": reverse("admin:sync_all")},
        ]

    @admin.action(description="Sync from stripe")
    def sync(self, request, queryset):
        self.stripe_model_action.sync_by_ids(
            queryset.values_list("stripe_id", flat=True)
        )

    def sync_all(self, request):
        self.stripe_model_action.sync_all()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def get_urls(self):
        urls = super().get_urls()
        action_urls = [
            path(
                "sync_all",
                self.admin_site.admin_view(self.sync_all),
                name="sync_all",
            ),
        ]
        return urls + action_urls

    def change_list_view(self, request, extra_context=None, *args, **kwargs):
        extra_context = extra_context or {}
        extra_context["action_buttons"] = self.get_action_buttons()

        # Optionally render the buttons from your app-specific template
        button_html = render_to_string(
            "admin/includes/change_list_buttons.html", extra_context
        )
        extra_context["button_html"] = button_html

        return super().changelist_view(
            request, extra_context=extra_context, *args, **kwargs
        )
