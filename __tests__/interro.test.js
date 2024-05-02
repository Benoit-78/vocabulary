// Import the function to be tested
const { nextGuess } = require('../src/static/scripts/interro.js');

describe('nextGuess', () => {
  // write a test case using it() to define a single test scenario
  it('should navigate to the correct URL with token, total, count, and score parameters', () => {
    // Store the original value of window.location.href
    const oldLocation = window.location.href;

    // Mock window.location.href
    const hrefSetter = jest.spyOn(window.location, 'href', 'set');
    nextGuess('sampleToken', 20, 5, 100);

    // Expect window.location.href to be updated with the correct URL
    expect(hrefSetter).toHaveBeenCalledWith('/interro/interro-question?token=sampleToken&total=20&count=5&score=100');

    // Restore window.location.href to its original value
    window.location.href = oldLocation;
  });
});
