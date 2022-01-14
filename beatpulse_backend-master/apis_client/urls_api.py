from dynamic_rest.routers import DynamicRouter

# from rest_framework_cache.registry import cache_registry
from apis_client.viewsets.viewset_beat import BeatViewSet
from apis_client.viewsets.viewset_beat_key import BeatKeyViewSet
from apis_client.viewsets.viewset_billing_info import BillingInfoViewSet
from apis_client.viewsets.viewset_cart_item import CartItemViewSet
from apis_client.viewsets.viewset_coupon import CouponViewSet
from apis_client.viewsets.viewset_deal import DealViewSet
from apis_client.viewsets.viewset_followed_playlist import FollowedPlaylistViewSet
from apis_client.viewsets.viewset_followed_producer import FollowedProducerViewSet
from apis_client.viewsets.viewset_license_option import LicenseOptionViewSet
from apis_client.viewsets.viewset_liked_beat import LikedBeatViewSet
from apis_client.viewsets.viewset_lyric import LyricViewSet
from apis_client.viewsets.viewset_order import OrderViewSet
from apis_client.viewsets.viewset_own_profile import OwnProfileViewSet
from apis_client.viewsets.viewset_producer import ProducerViewSet
from apis_client.viewsets.viewset_trending_beat import TrendingBeatViewsetViewSet
from apis_client.viewsets.viewsets_beat_groups import PlaylistViewSet, GenreViewSet, MoodViewSet

router = DynamicRouter()
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
router.register('followed_producers', FollowedProducerViewSet)
router.register('followed_playlists', FollowedPlaylistViewSet)
router.register('liked_beats', LikedBeatViewSet)
router.register('lyrics', LyricViewSet)
router.register('beat_keys', BeatKeyViewSet)
router.register('billing_infos', BillingInfoViewSet)
router.register('orders', OrderViewSet)
router.register('cart_items', CartItemViewSet)
