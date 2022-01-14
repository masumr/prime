from dynamic_rest.routers import DynamicRouter

from apis_admin.viewsets.viewset_account_invitation import AccountInvitationViewSet
from apis_admin.viewsets.viewset_beat import BeatViewSet
from apis_admin.viewsets.viewset_coupon import CouponViewSet
from apis_admin.viewsets.viewset_deal import DealViewSet
from apis_admin.viewsets.viewset_license_option import LicenseOptionViewSet
from apis_admin.viewsets.viewset_order import OrderViewSet
from apis_admin.viewsets.viewset_own_profile import OwnProfileViewSet
from apis_admin.viewsets.viewset_producer import ProducerViewSet
from apis_admin.viewsets.viewset_producer_payout import ProducerPayoutViewSet
from apis_admin.viewsets.viewset_profile import ProfileViewSet
from apis_admin.viewsets.viewset_trending_beat import TrendingBeatViewsetViewSet
from apis_admin.viewsets.viewsets_beat_groups import PlaylistViewSet, GenreViewSet, MoodViewSet
from apis_client.viewsets.viewset_beat_key import BeatKeyViewSet

router = DynamicRouter()
router.register('profiles', ProfileViewSet)
router.register('own_profile', OwnProfileViewSet)
router.register('playlists', PlaylistViewSet)
router.register('genres', GenreViewSet)
router.register('moods', MoodViewSet)
router.register('license_options', LicenseOptionViewSet)
router.register('producers', ProducerViewSet)
router.register('beats', BeatViewSet)
router.register('trending_beats', TrendingBeatViewsetViewSet)
router.register('coupons', CouponViewSet)
router.register('deals', DealViewSet)
router.register('beat_keys', BeatKeyViewSet)
router.register('producer_payouts', ProducerPayoutViewSet)
router.register('orders', OrderViewSet)
router.register('account_invitations', AccountInvitationViewSet)
