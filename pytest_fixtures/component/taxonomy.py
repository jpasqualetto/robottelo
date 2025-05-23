# Content Component fixtures
from manifester import Manifester
import pytest

from robottelo.config import settings
from robottelo.constants import DEFAULT_LOC, DEFAULT_ORG


@pytest.fixture(scope='session')
def default_org(session_target_sat):
    return session_target_sat.api.Organization().search(query={'search': f'name="{DEFAULT_ORG}"'})[
        0
    ]


@pytest.fixture(scope='session')
def default_location(session_target_sat):
    return session_target_sat.api.Location().search(query={'search': f'name="{DEFAULT_LOC}"'})[0]


@pytest.fixture
def current_sat_org(target_sat):
    """Return the current organization assigned to the Satellite host"""
    sat_host = target_sat.api.Host().search(query={'search': f'name={target_sat.hostname}'})[0]
    return sat_host.organization.read()


@pytest.fixture
def current_sat_location(target_sat):
    """Return the current location assigned to the Satellite host"""
    sat_host = target_sat.api.Host().search(query={'search': f'name={target_sat.hostname}'})[0]
    return sat_host.location.read()


@pytest.fixture
def function_org(target_sat):
    return target_sat.api.Organization().create()


@pytest.fixture(scope='module')
def module_org(module_target_sat):
    return module_target_sat.api.Organization().create()


@pytest.fixture(scope='class')
def class_org(class_target_sat):
    org = class_target_sat.api.Organization().create()
    yield org
    org.delete()


@pytest.fixture(scope='module')
def module_location(module_target_sat, module_org):
    return module_target_sat.api.Location(organization=[module_org]).create()


@pytest.fixture(scope='class')
def class_location(class_target_sat, class_org):
    loc = class_target_sat.api.Location(organization=[class_org]).create()
    yield loc
    loc.delete()


@pytest.fixture
def function_location(target_sat):
    return target_sat.api.Location().create()


@pytest.fixture
def function_location_with_org(target_sat, function_org):
    return target_sat.api.Location(organization=[function_org]).create()


@pytest.fixture(scope='module')
def module_sca_manifest_org(module_org, module_sca_manifest, module_target_sat):
    """Creates an organization and uploads an SCA mode manifest generated with manifester"""
    module_target_sat.upload_manifest(module_org.id, module_sca_manifest.content)
    return module_org


@pytest.fixture(scope='class')
def class_sca_manifest_org(class_org, class_sca_manifest, class_target_sat):
    """Creates an organization and uploads an SCA mode manifest generated with manifester"""
    class_target_sat.upload_manifest(class_org.id, class_sca_manifest.content)
    return class_org


@pytest.fixture
def sca_manifest_org_for_upgrade(function_org, sca_manifest_for_upgrade, target_sat):
    """A Pytest fixture that creates an organization and uploads an sca mode manifest
    generated with Manifester. This will be used for upgrade scenarios"""
    sca_manifest, _ = sca_manifest_for_upgrade
    target_sat.upload_manifest(function_org.id, sca_manifest.content)
    return function_org


@pytest.fixture
def function_sca_manifest_org(function_org, function_sca_manifest, target_sat):
    """Creates an organization and uploads an SCA mode manifest generated with manifester"""
    target_sat.upload_manifest(function_org.id, function_sca_manifest.content)
    return function_org


@pytest.fixture
def function_els_sca_manifest_org(function_org, function_sca_els_manifest, target_sat):
    """Creates an organization and uploads an SCA mode manifest generated with manifester"""
    target_sat.upload_manifest(function_org.id, function_sca_els_manifest.content)
    return function_org


@pytest.fixture(scope='module')
def module_els_sca_manifest_org(module_org, module_sca_els_manifest, module_target_sat):
    """Creates an organization and uploads an SCA mode manifest generated with manifester"""
    module_target_sat.upload_manifest(module_org.id, module_sca_els_manifest.content)
    return module_org


@pytest.fixture(scope='class')
def class_els_sca_manifest_org(class_org, class_sca_els_manifest, class_target_sat):
    """Creates an organization and uploads an SCA mode manifest generated with manifester"""
    class_target_sat.upload_manifest(class_org.id, class_sca_els_manifest.content)
    return class_org


# Note: Manifester should not be used with the Satellite QE RHSM account until
# subscription needs are scoped and sufficient subscriptions added to the
# Satellite QE RHSM account. Manifester can be safely used locally with personal
# or stage RHSM accounts.


@pytest.fixture(scope='session')
def session_sca_manifest():
    """Yields a manifest in entitlement mode with subscriptions determined by the
    `manifest_category.entitlement` setting in conf/manifest.yaml."""
    with Manifester(manifest_category=settings.manifest.golden_ticket) as manifest:
        yield manifest


@pytest.fixture(scope='module')
def module_extra_rhel_sca_manifest():
    """Yields a manifest in sca mode with subscriptions determined by the
    'manifest_category.extra_rhel_entitlement` setting in conf/manifest.yaml."""
    with Manifester(
        manifest_category=settings.manifest.extra_rhel_entitlement, simple_content_access="enabled"
    ) as manifest:
        yield manifest


@pytest.fixture(scope='module')
def module_sca_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.golden_ticket` setting in conf/manifest.yaml."""
    with Manifester(manifest_category=settings.manifest.golden_ticket) as manifest:
        yield manifest


@pytest.fixture(scope='class')
def class_sca_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.golden_ticket` setting in conf/manifest.yaml."""
    with Manifester(manifest_category=settings.manifest.golden_ticket) as manifest:
        yield manifest


@pytest.fixture
def function_sca_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.golden_ticket` setting in conf/manifest.yaml."""
    with Manifester(manifest_category=settings.manifest.golden_ticket) as manifest:
        yield manifest


@pytest.fixture
def second_function_sca_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.golden_ticket` setting in conf/manifest.yaml.
    A different one than is used in `function_sca_manifest_org`."""
    with Manifester(manifest_category=settings.manifest.golden_ticket) as manifest:
        yield manifest


@pytest.fixture(scope='module')
def module_sca_els_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.els_rhel_manifest` setting in conf/manifest.yaml."""
    with Manifester(manifest_category=settings.manifest.els_rhel_manifest) as manifest:
        yield manifest


@pytest.fixture(scope='class')
def class_sca_els_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.els_rhel_manifest` setting in conf/manifest.yaml."""
    with Manifester(manifest_category=settings.manifest.els_rhel_manifest) as manifest:
        yield manifest


@pytest.fixture
def function_sca_els_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.els_rhel_manifest` setting in conf/manifest.yaml."""
    with Manifester(manifest_category=settings.manifest.els_rhel_manifest) as manifest:
        yield manifest


@pytest.fixture(scope='module')
def smart_proxy_location(module_org, module_target_sat, default_smart_proxy):
    location = module_target_sat.api.Location(organization=[module_org]).create()
    default_smart_proxy.location.append(module_target_sat.api.Location(id=location.id))
    default_smart_proxy.update(['location'])
    return location


@pytest.fixture
def upgrade_entitlement_manifest():
    """Returns a manifest in entitlement mode with subscriptions determined by the
    `manifest_category.entitlement` setting in conf/manifest.yaml. used only for
    upgrade scenarios"""
    manifester = Manifester(manifest_category=settings.manifest.entitlement)
    return manifester.get_manifest(), manifester


@pytest.fixture
def sca_manifest_for_upgrade():
    """Returns a manifest in sca mode. Used only for upgrade scenarios"""
    manifester = Manifester(manifest_category=settings.manifest.golden_ticket)
    return manifester.get_manifest(), manifester


@pytest.fixture
def func_future_dated_subscription_manifest(target_sat, function_org):
    """Create and upload future date subscription manifest into org"""
    with Manifester(manifest_category=settings.manifest.future_date_subscription) as manifest:
        target_sat.upload_manifest(function_org.id, manifest.content)
    return manifest
