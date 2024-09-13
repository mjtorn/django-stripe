Changelog
=============

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
-------------------
### Added

* `StripeAbstractCard` abstract model that simplifies the integration with Stripe Card.
* `StripeCard` model that will store stripe card data.
* `StripeCardAction` action that will sync card data from stripe.


## [0.1.0] - 2024-09-20
-----------------------
### Added
* Stripe Abstract Model: `StripeAbstractCustomer`,
  `StripeAbstractEvent`, `StripeAbstractProduct`,
  `StripeAbstractPrice`, and `StripeAbstractSubscription`
  abstract models that simplify the integration with Stripe.
* Stripe Models: `StripeCustomer`, `StripeEvent`, `StripeCard`,
  `StripeProduct`, `StripePrice`, and `StripeSubscription`
  models that simplify the integration with Stripe.
* Stripe Action Mixin: `StripeSyncActionMixin`,
  `StripeSoftDeleteMixin` mixins that simplify the integration
  with Stripe.
* Stripe Actions: `StripeCustomerAction`,
  `StripeSubscriptionAction`, `StripeEventAction`,
  `StripeCouponAction`, `StripePriceAction` and
  `StripeProductAction` actions that simplify the integration
  with Stripe.
* Stripe Abstract Webhook: `StripeWebhook` class that provides a
  simple and flexible way to process incoming webhook requests.
* Stripe Webhooks: `CustomerCreatedWebhook`,
  `CustomerUpdatedWebhook`, `CustomerDeletedWebhook`,
  `SubscriptionCreatedWebhook`, `SubscriptionUpdatedWebhook`,
  `SubscriptionDeletedWebhook`, `SubscriptionTrialWillEndWebhook`,
  `ProductCreatedWebhook`, `ProductUpdatedWebhook`, `ProductDeletedWebhook`
  `PriceCreatedWebhook`, `PriceUpdatedWebhook`, `PriceDeletedWebhook`,
  `CouponCreatedWebhook`, `CouponUpdatedWebhook`, `CouponDeletedWebhook`,
  webhooks that simplify the
  integration with Stripe.
