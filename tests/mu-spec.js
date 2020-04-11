var fake_mu = mu("editor");

describe("An editor for begginer Python programmers", function() {

    describe("The editor initialises as expected.", function() {
        it("The editor is associated with the expected referenced DOM object.",
            function() {
                var editor = mu("editor")
                expect(editor).toBeDefined();
        });
    });
});
