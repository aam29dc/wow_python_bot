local isDataVis = false

-- Create the frame for displaying data
local dataFrame = CreateFrame("Frame", "posFrame", UIParent, "TranslucentFrameTemplate")
dataFrame:SetSize(325, 330)
dataFrame:SetPoint("CENTER", UIParent, "CENTER", 0, 10)
dataFrame:Hide()

-- Create font strings for each stat
local hpText = dataFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
hpText:SetPoint("TOPLEFT", dataFrame, "TOPLEFT", 10, -15)
hpText:SetTextColor(1, 1, 1)
hpText:SetAlpha(1)
hpText:SetFont("Fonts\\FRIZQT__.TTF", 22, "OUTLINE")
hpText:SetShadowOffset(2, -2)
hpText:SetShadowColor(0, 0, 0, 1)

local powerText = dataFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
powerText:SetPoint("TOPLEFT", hpText, "BOTTOMLEFT", 0, -5)
powerText:SetTextColor(1, 1, 1)
powerText:SetAlpha(1)
powerText:SetFont("Fonts\\FRIZQT__.TTF", 22, "OUTLINE")
powerText:SetShadowOffset(2, -2)
powerText:SetShadowColor(0, 0, 0, 1)

local positionXText = dataFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
positionXText:SetPoint("TOPLEFT", powerText, "BOTTOMLEFT", 0, -5)
positionXText:SetTextColor(1, 1, 1)
positionXText:SetAlpha(1)
positionXText:SetFont("Fonts\\FRIZQT__.TTF", 22, "OUTLINE")
positionXText:SetShadowOffset(2, -2)
positionXText:SetShadowColor(0, 0, 0, 1)

local positionYText = dataFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
positionYText:SetPoint("TOPLEFT", positionXText, "BOTTOMLEFT", 0, -5)
positionYText:SetTextColor(1, 1, 1)
positionYText:SetAlpha(1)
positionYText:SetFont("Fonts\\FRIZQT__.TTF", 22, "OUTLINE")
positionYText:SetShadowOffset(2, -2)
positionYText:SetShadowColor(0, 0, 0, 1)

local targetText = dataFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
targetText:SetPoint("TOPLEFT", positionYText, "BOTTOMLEFT", 0, -5)
targetText:SetTextColor(1, 1, 1)
targetText:SetAlpha(1)
targetText:SetFont("Fonts\\FRIZQT__.TTF", 22, "OUTLINE")
targetText:SetShadowOffset(2, -2)
targetText:SetShadowColor(0, 0, 0, 1)

local castingText = dataFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
castingText:SetPoint("TOPLEFT", targetText, "BOTTOMLEFT", 0, -5)
castingText:SetTextColor(1, 1, 1)
castingText:SetAlpha(1)
castingText:SetFont("Fonts\\FRIZQT__.TTF", 20, "OUTLINE")
castingText:SetShadowOffset(2, -2)
castingText:SetShadowColor(0, 0, 0, 1)

-- Function to update the stats
local function UpdateStats()
    -- Get health and power percentages
    local hpPercent = (UnitHealth("player") / UnitHealthMax("player")) * 100
    local powerPercent = (UnitPower("player") / UnitPowerMax("player")) * 100

    -- Get player position
    local playerMap = C_Map.GetBestMapForUnit("player")
    local px, py = C_Map.GetPlayerMapPosition(playerMap, "player"):GetXY()
    px = px * 100
    py = py * 100

    -- Check if target is attackable and if it is dead
    local targetExists = UnitExists("target")
    local isEnemy = targetExists and UnitCanAttack("player", "target")
    local isDead = targetExists and UnitIsDead("target")

    -- Check if player is casting
    local isCasting = UnitCastingInfo("player")
    local castingStatus = isCasting and "T" or "F" -- If casting, show "T" else "F"

    -- Update the text for each stat
    hpText:SetText(string.format(" H = %.2f", hpPercent))
    powerText:SetText(string.format(" P = %.2f", powerPercent))
    positionXText:SetText(string.format(" X = %.2f", px))
    positionYText:SetText(string.format(" Y = %.2f", py))

    -- Update the target status (Dead, Enemy, Friendly, No target)
    if isDead then
        targetText:SetText(" T = D")
    else
        targetText:SetText(string.format(" T = %s", targetExists and (isEnemy and "E" or "F") or "N"))
    end

    -- Update casting status (T for casting, F for not casting)
    castingText:SetText(string.format(" C = %s", castingStatus))
end

-- Toggle the visibility of the data frame
local function TogglePosDisplay()
    if isDataVis then
        dataFrame:Hide()
    else
        UpdateStats()
        dataFrame:Show()
    end
    isDataVis = not isDataVis
end

-- Slash command to toggle visibility
SLASH_STATS1 = "/stats"
SlashCmdList["STATS"] = TogglePosDisplay

-- Update stats on every frame
dataFrame:SetScript("OnUpdate", function(self, elapsed)
    if isDataVis then
        UpdateStats()
    end
end)