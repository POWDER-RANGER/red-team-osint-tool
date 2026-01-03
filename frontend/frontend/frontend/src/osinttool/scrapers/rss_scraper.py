# osinttool/scrapers/rss_scraper.py
import feedparser
import re
from osinttool.db_writer import SourceRegistry, EvidenceWriter, AlertDispatcher

class RSSScraperIntegrated:
    """RSS scraper with database integration"""
    
    def __init__(self, name, feed_url, watchlist):
        self.name = name
        self.feed_url = feed_url
        self.watchlist = watchlist  # List of keywords/indicators to watch
        
        # Register source in database
        self.source_id = SourceRegistry.register(
            name=self.name,
            source_type='rss',
            url=self.feed_url,
            config={'watchlist': self.watchlist}
        )
    
    def run(self):
        """Execute scraper and write to database"""
        print(f"[*] Running RSS scraper: {self.name}")
        
        # Update status to active
        SourceRegistry.update_status(self.source_id, 'active')
        
        try:
            # Fetch and parse feed
            feed = feedparser.parse(self.feed_url)
            
            for entry in feed.entries:
                title = entry.get('title', 'No Title')
                content = entry.get('summary', entry.get('description', ''))
                url = entry.get('link', '')
                
                # Extract IOCs (simple regex examples)
                iocs = self._extract_iocs(content)
                
                # Check if content matches watchlist
                matched = self._check_watchlist(content)
                
                # Determine severity
                severity = 'critical' if matched else 'info'
                
                # Write to database
                evidence_id = EvidenceWriter.write(
                    source_id=self.source_id,
                    title=title,
                    content=content,
                    url=url,
                    severity=severity,
                    matched=matched,
                    iocs=iocs,
                    tags=['rss', 'security_news']
                )
                
                # Dispatch alerts for matched evidence
                if matched and evidence_id:
                    self._dispatch_alert(evidence_id, title, content)
            
            # Update status to idle (success)
            SourceRegistry.update_status(self.source_id, 'idle')
            print(f"[✓] RSS scraper complete: {len(feed.entries)} entries processed")
            
        except Exception as e:
            SourceRegistry.update_status(self.source_id, 'error')
            print(f"[✗] RSS scraper error: {e}")
    
    def _extract_iocs(self, text):
        """Extract indicators of compromise"""
        iocs = []
        
        # IP addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        iocs.extend(re.findall(ip_pattern, text))
        
        # Domain names
        domain_pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b'
        iocs.extend(re.findall(domain_pattern, text.lower()))
        
        # SHA256 hashes
        hash_pattern = r'\b[a-f0-9]{64}\b'
        iocs.extend(re.findall(hash_pattern, text.lower()))
        
        return list(set(iocs))  # Remove duplicates
    
    def _check_watchlist(self, text):
        """Check if text contains watchlist items"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.watchlist)
    
    def _dispatch_alert(self, evidence_id, title, content):
        """Dispatch alerts for critical findings"""
        message = f"🚨 MATCHED EVIDENCE\n\nTitle: {title}\n\nPreview: {content[:200]}..."
        
        # Log Slack alert
        AlertDispatcher.log(
            evidence_id=evidence_id,
            channel='slack',
            recipient='#security-alerts',
            message=message,
            status='sent'
        )
        
        print(f"[🚨] Alert dispatched for evidence ID {evidence_id}")


# Example usage
if __name__ == "__main__":
    scraper = RSSScraperIntegrated(
        name="ThreatPost Security News",
        feed_url="https://threatpost.com/feed/",
        watchlist=["exploit", "vulnerability", "breach", "0day"]
    )
    scraper.run()
