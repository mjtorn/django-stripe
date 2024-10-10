# Third Party Stuff
from django.contrib import admin, messages
from django.urls import path, reverse, reverse_lazy
from django.http import HttpResponseRedirect


class AbstractStripeModelAdmin(admin.ModelAdmin):
    stripe_model_action = None
    actions = ["sync"]
    change_list_template = "change_list.html"
    change_form_template = "change_form.html"

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

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
        change_list_link = reverse(
            "admin:%s_%s_changelist"
            % (self.model._meta.app_label, self.model._meta.model_name)
        )
        return [
            {
                "label": "Sync all objects from stripe",
                "url": f"{change_list_link}sync_all/",
            },
        ]

    def sync_object(self, request, object_id):
        obj = self.get_object(request, object_id)
        if obj:
            if self.stripe_model_action:
                self.stripe_model_action.sync_by_ids([obj.stripe_id])
                messages.success(request, "Object synced with Stripe successfully.")
            else:
                messages.error(request, "Stripe model action not defined.")
        else:
            messages.error(request, "Object not found.")

        return HttpResponseRedirect(
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
                args=[object_id],
            )
        )

    @admin.action(description="Sync from stripe")
    def sync(self, request, queryset):
        self.stripe_model_action.sync_by_ids(
            queryset.values_list("stripe_id", flat=True)
        )

    def sync_all(self, request):
        if self.stripe_model_action is not None:
            self.stripe_model_action.sync_all()
            messages.success(request, "Synced all objects from stripe")
        else:
            messages.error(request, "Stripe model action not defined.")
        change_list_link = reverse_lazy(
            "admin:%s_%s_changelist"
            % (self.model._meta.app_label, self.model._meta.model_name)
        )
        return HttpResponseRedirect(change_list_link)

    def get_urls(self):
        urls = super().get_urls()
        action_urls = [
            path("sync_all/", self.sync_all),
            path(
                "<uuid:object_id>/sync/",
                self.admin_site.admin_view(self.sync_object),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_sync_object",
            ),
        ]
        return action_urls + urls

    def changelist_view(self, request, extra_context=None, *args, **kwargs):
        extra_context = extra_context or {}
        extra_context["action_buttons"] = self.get_action_buttons()

        return super().changelist_view(
            request, extra_context=extra_context, *args, **kwargs
        )
