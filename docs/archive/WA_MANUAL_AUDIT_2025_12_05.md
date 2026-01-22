# WA Councils Requiring Manual Audit (5 December 2025)

This document lists all Western Australian councils from `wa_selector_report.json` that require manual attention due to missing selectors, errors, or invalid sample data. These councils could not be auto-configured and need further investigation to restore news coverage.

## Criteria for Manual Audit
- All selectors are null
- Error field present
- Sample data is missing or appears invalid (e.g., generic text, contact info, navigation labels)

---

## Councils with Null Selectors or Errors

| Council ID | Issue Type | Details |
|------------|------------|---------|
| bayswater | error | Connection reset by peer |
| quairading | error | SSL protocol error |
| carnamah | null selectors | All selectors null |
| collie | null selectors | All selectors null |
| coorow | null selectors | All selectors null |
| cranbrook | null selectors | All selectors null |
| denmark | null selectors | All selectors null |
| fremantle | null selectors | All selectors null |
| halls-creek | null selectors | All selectors null |
| irwin | null selectors | All selectors null |
| karratha | null selectors | All selectors null |
| kent | null selectors | All selectors null |
| manjimup | null selectors | All selectors null |
| mosman-park | null selectors | All selectors null |
| mount-marshall | null selectors | All selectors null |
| mukinbudin | null selectors | All selectors null |
| sandstone | null selectors | All selectors null |
| three-springs | null selectors | All selectors null |
| wanneroo | null selectors | All selectors null |

---

## Councils with Invalid Sample Data (Generic/Navigation/Contact)

| Council ID | Sample Title | Sample Date | Sample Link |
|------------|--------------|------------|-------------|
| armadale | Skip to content | null | /service |
| augusta-margaret-river | Skip to content | Search | / |
| belmont | Skip to content | 60 | # |
| beverley | Skip to Content | Accessibility | #maincontent |
| broome | opens in new tab or window | opens in new tab or window | /404-Error-page?OC_EA_EmergencyAnnouncementList_Dismiss=ccb42616-1e61-4d5d-b514-2aa06bf20ff3 |
| bunbury | Skip to main content | Skip to main content | #main |
| cambridge | opens in new tab or window | opens in new tab or window | #main-content |
| claremont | Server Error | null | null |
| coolgardie | Bluebush Village |  | https://bluebushvillage.com.au/ |
| cuballing | Shire of Cuballing Email | Shire of Cuballing Email | mailto:enquiries@cuballing.wa.gov.au |
| cunderdin | Contrast | Contrast | javascript:void(0) |
| dandaragan | Home | Home | javascript:void(1234) |
| dardanup | Accessibility | Accessibility | mailto:records@dardanup.wa.gov.au |
| dumbleyung | top of page | top of page | tel:08 9863 4012 |
| exmouth | Contact us | Phone: (08) 9949 3000 | / |
| goomalling | Accessibility | Accessibility | tel:0896291101 |
| koorda | A+ | | javascript:void(2) |
| melville | Close alert | Close alert | #content |
| mingenew | Skip to content | 39°C | #content |
| moora | MOORA WEATHER | Accessibility | / |
| mount-magnet | 0 | 0 | /cart |
| nannup | Accessibility | Accessibility | tel:0897561018 |
| narembeen | (08) 9064 7308 | (08) 9064 7308 | tel:0890647308 |
| narrogin | A+ | Facebook | tel:9890 0900 |
| northam | Translation |  | / |
| nungarin | Nungarin | Search | / |
| peppermint-grove | A- |  | / |
| perenjori | Accessibility | Accessibility | javascript:void(11); |
| perth | Enable JavaScript and cookies to continue | Enable JavaScript and cookies to continue | null |
| pingelly | Facebook | Facebook | https://www.facebook.com/Shire-of-Pingelly-200065203727/ |
| plantagenet | High Contrast | High Contrast | / |
| port-hedland | Select | Select | / |
| ravensthorpe | Weather | Weather | mailto:shire@ravensthorpe.wa.gov.au |
| serpentine-jarrahdale | A+ | Prohibited Burning Period | javascript:void(13) |
| south-perth | Skip to main content | Search | #main |
| stirling | Skip to content | Skip to content | #content |
| subiaco | Skip to content |  | # |
| swan | Skip to Content | Skip to Content | #content |
| tammin | Skip to Content | Skip to Content | #content |
| trayning | High Contrast | High Contrast | / |
| victoria-park | Accessibility | Accessibility | /accessibility.aspx |
| victoria-plains | Accessibility | Accessibility | tel:0896287004 |
| wagin | Phone | Phone | /home.aspx |
| wongan-ballidu | Toggle mobile search | Toggle mobile search | / |
| woodanilling | Email | Email | tel:0898231506 |
| wyalkatchem | 9681 1166 | 9681 1166 | tel:0896811166 |
| york | Make text bigger | Make text bigger | / |

---

## Next Steps
- Manual review and correction of selectors, sample data, and platform detection for listed councils.
- Consider advanced platform detection, dry scraping, or direct contact for persistent cases.
- Update configs after manual fixes.
