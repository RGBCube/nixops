from tests.functional import DatabaseUsingTest


class TestQueryDeployments(DatabaseUsingTest):
    def test_shows_all_deployments(self):
        depls = [self.sf.create_deployment() for _ in range(10)]
        uuids = self.sf.query_deployments()
        for depl in depls:
            assert any(depl.uuid == uuid for uuid in uuids)
