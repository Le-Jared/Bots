// ==UserScript==
// @name         TicketMaster
// @namespace    http://tampermonkey.net/
// @version      0.4
// @description  Fast execution of reserving tickets in cart
// @match        https://www1.ticketmaster.co.uk/*
// @match        https://www1.ticketmaster.com/*
// @match        https://www1.ticketmaster.sg/*
// @require      https://code.jquery.com/jquery-2.1.3.min.js
// @grant        none
// ==/UserScript==

(async function() {
    'use strict';

    const refreshIntervalSeconds = 1;
    const numberOfTickets = 2;
    const apiKey = "YOUR_2CAPTCHA_API_KEY";  // Replace with your 2Captcha API Key
    const siteKey = "YOUR_SITE_KEY"; // Replace this with the site key from TicketMaster
    const pageUrl = window.location.href; // Current page URL

    const getElementByXpath = path => {
        return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    };

    const clickElement = path => {
        const element = getElementByXpath(path);
        if(element && typeof element.click === 'function') {
            element.click();
            return element;
        }
        return null;
    };

    const waitForElement = (selector, callback) => {
        if (jQuery(selector).length) {
            callback();
        } else {
            setTimeout(() => {
                waitForElement(selector, callback);
            }, 100);
        }
    };

    // Define CAPTCHA-solving function
    async function solveCaptcha() {
        try {
            const response = await fetch(`https://2captcha.com/in.php?key=${apiKey}&method=userrecaptcha&googlekey=${siteKey}&pageurl=${pageUrl}&json=1`);
            const data = await response.json();

            if(!data.status) {
                console.error('Error:', (data.error_text !== undefined) ? data.error_text : data.request);
                return;
            }

            let intervalId = setInterval(async () => {
                const captchaResponse = await fetch(`https://2captcha.com/res.php?key=${apiKey}&action=get&id=${data.request}&json=1`);
                const captchaData = await captchaResponse.json();

                if(captchaData.status && captchaData.request !== "CAPCHA_NOT_READY") {
                    clearInterval(intervalId);
                    document.querySelector('#g-recaptcha-response').innerHTML = captchaData.request;
                    console.log('CAPTCHA solved, you may submit the form');
                } else if(!captchaData.status) {
                    clearInterval(intervalId);
                    console.error('Error:', (captchaData.error_text !== undefined) ? captchaData.error_text : captchaData.request);
                }
            }, 5000);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Functions related to the TicketMaster script...
    function skipPopup() {
        const popupPresent = getElementByXpath('//button[@class = "modal-dialog__button landing-modal-footer__skip-button"]');
        if(popupPresent) {
            try{ 
                popupPresent.click(); 
            } catch(ex){ 
                console.error('Error:', ex); 
            }
        }
    }

    function checkForFilterPanel() {
        return getElementByXpath('//div[@class = "filter-bar__content"]');  
    }

    function processFilterPanel(filterBar) {
        clickElement('(//ul/li[@class = "quick-picks__list-item"])[1]/div/div');
        waitForElement('.offer-card', function() {
            changeTicketQuantity();
            clickElement('//button[@id = "offer-card-buy-button"]');
            waitForElement('.button-aux, .modal-dialog__button', function() {
                const sectionChangeBuyButton = getElementByXpath('//button[@class = "button-aux modal-dialog__button"]');
                sectionChangeBuyButton.click();
            });
        });
    }

    function changeTicketQuantity() {
        const rightPanelCurrentTicketCountElement = getElementByXpath('//div[@class = "qty-picker__number qty-picker__number--lg"]');
        const currentTicketCount = rightPanelCurrentTicketCountElement.innerText;

        let ticketQuantityDifference = numberOfTickets - currentTicketCount;
        if (ticketQuantityDifference > 0) {
            const ticketIncrementElement = clickElement('//button[@class = "qty-picker__button qty-picker__button--increment qty-picker__button--lg"]');
            for (let i = 0; i < ticketQuantityDifference; i++) {
                try{ 
                    ticketIncrementElement.click(); 
                } catch(ex){ 
                    console.error('Error:', ex); 
                }
            }
        } else if(ticketQuantityDifference < 0) {
            ticketQuantityDifference = Math.abs(ticketQuantityDifference);
            const ticketDecrementElement = clickElement('//button[@class = "qty-picker__button qty-picker__button--decrement qty-picker__button--lg"]');
            for (let i = 0; i < ticketQuantityDifference; i++) {
                try{ 
                    ticketDecrementElement.click(); 
                } catch(ex){ 
                    console.error('Error:', ex); 
                }
            }
        }
    }

    function checkForGeneralAdmission() {
        return getElementByXpath('//button[@id = "offer-card-buy-button"]');
    }

    function processGeneralAdmission(generalAdmissionBuyButton) {
        changeTicketQuantity();
        generalAdmissionBuyButton.click();  
    }

    function reload() {
        window.top.location.reload();
    }

    // Call all your functions inside the document ready function
    $(document).ready(async () => {
        let success = false;
        skipPopup();

        try {
            const filterBar = checkForFilterPanel();
            if(filterBar) {
                console.log('These tickets have a filter bar');
                success = true;
                processFilterPanel(filterBar);
            }
        } catch (error) {
            console.error('Error in processing tickets with a filter bar:', error);
        }

        try {
            const generalAdmissionBuyButton = checkForGeneralAdmission();
            if(generalAdmissionBuyButton) {
                console.log('These tickets are General Admission');
                success = true;
                processGeneralAdmission(generalAdmissionBuyButton);
            }
        } catch (error) {
            console.error('Error in processing General Admission tickets:', error);
        }

        // If captcha is presented
        await solveCaptcha();

        if(!success) {
            setTimeout(() => { reload(); }, refreshIntervalSeconds * 1000); 
        }
    });
})();

