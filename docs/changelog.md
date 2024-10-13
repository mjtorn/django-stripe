Changelog
=============

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
-------------------
### Added
* `StripeCard` model that will store stripe card data.
* `StripeCardAction` action that will sync card data from stripe.


## [0.2.0] - 2024-09-16
-------------------
### Added
* `StripeCustomerAdmin` admin class that will display stripe customer data.
* `StripeEventAdmin` admin class that will display stripe event data.
* `StripeProductAdmin` admin class that will display stripe product data.
* `StripePriceAdmin` admin class that will display stripe price data.
* `StripeCouponAdmin` admin class that will display stripe coupons data.
* `StripeSubscriptionAdmin` admin class that will display stripe subscription data.

### Fixed
* Sync for `StripePriceAction` failing.


## [0.1.1] - 2024-09-16
-----------------------
### Added
  - **Stripe Models:** The following models have been added to simplify
    the integration with Stripe.
    - `StripeCustomer` model that will store stripe customer data.
    - `StripeEvent` model that will store stripe event data.
    - `StripeProduct` model that will store stripe product data.
    - `StripePrice` model that will store stripe price data.
    - `StripeSubscription` model that will store stripe subscription data.

  - **Stripe Action Mixin:** `StripeSyncActionMixin` and
    `StripeSoftDeleteMixin` mixins that simplify the integration
    with Stripe.
    - `StripeSyncActionMixin` mixin that provides a sync method
      that will sync the local database with the stripe data.
    - `StripeSoftDeleteMixin` mixin that provides soft delete
      method that will soft delete the stripe object in local database.

  - **Stripe Actions:** The following actions are provided to help
    with syncing local database with stripe data.
    - `StripeCustomerAction` action that syncs the local
      database with the stripe customer data.
    - `StripeSubscriptionAction` action that syncs the local
      database with the stripe subscription data.
    - `StripeEventAction` action that syncs the local
      database with the stripe event data.
    - `StripeCouponAction` action that syncs the local
      database with the stripe coupon data.
    - `StripePriceAction` action that syncs the local
      database with the stripe price data.
    - `StripeProductAction` action that syncs the local
      database with the stripe product data.

  - **Stripe Abstract Webhook:** `StripeWebhook` class that provides a
    simple and flexible way to process incoming webhook requests.

  - **Stripe Webhooks:**
    - Customer Webhook
        - `CustomerCreatedWebhook` to process customer created event.
        - `CustomerUpdatedWebhook` to process customer updated event.
        - `CustomerDeletedWebhook` to process customer deleted event.
    - Subscription Webhook
        - `SubscriptionCreatedWebhook` to process subscription created event.
        - `SubscriptionUpdatedWebhook` to process subscription updated event.
        - `SubscriptionDeletedWebhook` to process subscription deleted event.
        - `SubscriptionTrialWillEndWebhook` to process subscription trial will end event.
    - Product Webhook
        - `ProductCreatedWebhook` to process product created event.
        - `ProductUpdatedWebhook` to process product updated event.
        - `ProductDeletedWebhook` to process product deleted event.
    - Price Webhook
        - `PriceCreatedWebhook` to process price created event.
        - `PriceUpdatedWebhook` to process price updated event.
        - `PriceDeletedWebhook` to process price deleted event.
    - Coupon Webhook
        - `CouponCreatedWebhook` to process coupon created event.
        - `CouponUpdatedWebhook` to process coupon updated event.
        - `CouponDeletedWebhook` to process coupon deleted event.
