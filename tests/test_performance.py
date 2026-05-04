import time, pytest

class TestPerformance:
    def test_router_micro_under_100ms(self, router):
        start = time.time()
        router.route("classify_element", {})
        assert (time.time()-start)*1000 < 100

    def test_router_mid_under_500ms(self, router):
        start = time.time()
        router.route("classify_page", {"page_complexity": "low"})
        assert (time.time()-start)*1000 < 500

    def test_survey_mas_under_2000ms(self, router, link):
        from stealth_axiom.survey_mas import SurveyOrchestrator
        orch = SurveyOrchestrator(router, link)
        start = time.time()
        orch.run({"ax_tree": "... AXRadioButton ...", "body": "Frage 1"})
        assert (time.time()-start)*1000 < 2000
