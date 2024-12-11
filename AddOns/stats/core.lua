local isDataVis = false

-- Create the frame for displaying data
local dataFrame = CreateFrame("Frame", "posFrame", UIParent, "TranslucentFrameTemplate")
dataFrame:SetSize(325, 330)
dataFrame:SetPoint("CENTER", UIParent, "CENTER", 0, 10)
dataFrame:Hide()

-- Helper function to create font strings
local function CreateStatText(parent, anchor, rel, xOffset, yOffset)
    local statText = parent:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    statText:SetPoint("TOPLEFT", anchor, rel or "BOTTOMLEFT", xOffset or 0, yOffset or -5)
    statText:SetTextColor(1, 1, 1)
    statText:SetAlpha(1)
    statText:SetFont("Fonts\\FRIZQT__.TTF", 26, "OUTLINE")
    statText:SetShadowOffset(2, -2)
    statText:SetShadowColor(0, 0, 0, 1)
    return statText
end

-- Create font strings for each stat using the helper function
local hpText = CreateStatText(dataFrame, dataFrame, "TOPLEFT", 10, -15)
local powerText = CreateStatText(dataFrame, hpText)
local positionXText = CreateStatText(dataFrame, powerText)
local positionYText = CreateStatText(dataFrame, positionXText)
local angleText = CreateStatText(dataFrame, positionYText)

local targetText = CreateStatText(dataFrame, angleText)
local castingText = CreateStatText(dataFrame, targetText)

--[[
    Errors: map coords are from (0,0) to (1,1), if player goes outside this region the addon turns off
]]--

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

    -- Get player angle
    local playerAngle = GetPlayerFacing()

    -- Get if target is attackable and if it is dead
    local targetExists = UnitExists("target")
    local isEnemy = targetExists and UnitCanAttack("player", "target")
    local isDead = targetExists and UnitIsDead("target")

    -- Get if player is casting
    local castingStatus = UnitCastingInfo("player") and "T" or "F" -- If casting, show "T" else "F"

    -- Update the text for each stat
    local fractHP = string.gsub(hpPercent % 1, "0%.", "")
    hpText:SetText(string.format(" H=%d.%s", math.floor(hpPercent), string.sub(fractHP, 1, 2)))

    local fractPower = string.gsub(powerPercent % 1, "0%.", "")
    powerText:SetText(string.format(" P=%d.%s", math.floor(powerPercent), string.sub(fractPower, 1, 2)))
    -- max #s after . is 15
    local fractX = string.gsub(px % 1, "0%.", "")
    positionXText:SetText(string.format(" X=%d.%s", math.floor(px), string.sub(fractX, 1, 12)))

    local fractY = string.gsub(py % 1, "0%.", "")
    positionYText:SetText(string.format(" Y=%d.%s", math.floor(py), string.sub(fractY, 1, 12)))

    if isDead then
        targetText:SetText(" T=D")
    else
        targetText:SetText(string.format(" T=%s", targetExists and (isEnemy and "E" or "F") or "N"))
    end

    castingText:SetText(string.format(" C=%s", castingStatus))

    local fractAngle = string.gsub(playerAngle % 1, "0%.", "")
    angleText:SetText(string.format(" A=%d.%s", math.floor(playerAngle), string.sub(fractAngle, 1, 12)))
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

local function getZcoord()
    print(UnitPosition("player"))
    local mapID = C_Map.GetBestMapForUnit("player")
    local pos = C_Map.GetPlayerMapPosition(mapID, "player")
    local continentID, worldPos = C_Map.GetWorldPosFromMapPos(mapID, pos)
    print("Continent ID:", continentID, "World Position:", "x =", worldPos.x, "y =", worldPos.y, "z =", worldPos.z)
    print("You are in ", C_Map.GetMapInfo(mapID).name, mapID)
    print(mapID)
    print("Player's angle (in radians): ", GetPlayerFacing())
end

-- Slash command to toggle visibility
SLASH_STATS1 = "/stats"
SlashCmdList["STATS"] = TogglePosDisplay

SLASH_Z1 = "/z"
SlashCmdList["Z"] = getZcoord

-- Update stats on every frame
dataFrame:SetScript("OnUpdate", function(self, elapsed)
    if isDataVis then
        UpdateStats()
    end
end)