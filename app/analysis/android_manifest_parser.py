import xml.etree.ElementTree as ET
from pathlib import Path


class ManifestParser:
    """Parse Android Manifest file"""
    
    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        self.tree = None
        self.root = None
        self._parse()
    
    def _parse(self):
        """Parse manifest XML"""
        try:
            self.tree = ET.parse(self.manifest_path)
            self.root = self.tree.getroot()
        except Exception as e:
            print(f"Error parsing manifest: {e}")
    
    def get_permissions(self):
        """Get all permissions"""
        if not self.root:
            return []
        
        permissions = []
        for perm in self.root.findall('./uses-permission'):
            perm_name = perm.get('{http://schemas.android.com/apk/res/android}name', '')
            permissions.append(perm_name)
        return permissions
    
    def get_activities(self):
        """Get all activities"""
        if not self.root:
            return []
        
        activities = []
        for activity in self.root.findall('.//activity'):
            activity_name = activity.get('{http://schemas.android.com/apk/res/android}name', '')
            activities.append(activity_name)
        return activities
    
    def get_services(self):
        """Get all services"""
        if not self.root:
            return []
        
        services = []
        for service in self.root.findall('.//service'):
            service_name = service.get('{http://schemas.android.com/apk/res/android}name', '')
            services.append(service_name)
        return services
    
    def get_broadcast_receivers(self):
        """Get all broadcast receivers"""
        if not self.root:
            return []
        
        receivers = []
        for receiver in self.root.findall('.//receiver'):
            receiver_name = receiver.get('{http://schemas.android.com/apk/res/android}name', '')
            receivers.append(receiver_name)
        return receivers
    
    def get_content_providers(self):
        """Get all content providers"""
        if not self.root:
            return []
        
        providers = []
        for provider in self.root.findall('.//provider'):
            provider_name = provider.get('{http://schemas.android.com/apk/res/android}name', '')
            providers.append(provider_name)
        return providers
    
    def has_exported_components(self):
        """Check if any components are exported"""
        if not self.root:
            return False
        
        for component in self.root.findall('.//*'):
            exported = component.get('{http://schemas.android.com/apk/res/android}exported', '')
            if exported == 'true':
                return True
        return False
