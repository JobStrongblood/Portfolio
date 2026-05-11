/*
Job Wohali

 GAME NAME: Setup Wizard 

 GAMEPLAY DESCRIPTION:
 Controls:
 w - up
 a - left
 s down
 d - right
 p - fire
 Shoot fireballs at a rogue code target that appears on the screen. The main "targ"
 is a corrupted program represented by the garbled code:
 
 if(x!=y){
 null++
 }//err
 
 Your goal is to shoot this targ with your fireballs to "debug" it. Each hit
 teleports the targ and advances it downward.
 Hitting the targ will spawn a coin; collect it by navigating to it with your character!
 The wizard cannot move off-screen; he wraps around like in classic Mario games.                                                                                                                                                                                           
 Note: fireball collision triggers targ relocation and coin spawning.
 
 GAME LORE
 Setup Wizard, the master of user experience and vanquisher of the evil Terminal UI,
 stands ready to defend the digital realm. Armed with a magical staff and a
 command of code, he battles rogue programs, rogue enemies, and anything that
 dares corrupt the screen. His mission: maintain order, defeat chaos, and
 launch fireballs with precision.
 
 You're a wizard, Harry. Good luck!
 */

/* void drawTarg()
=== FUNCTION DESCRIPTION ===
Draws the target, "targ", which is made of text resembling 
garbled code. 
=== PARAMETERS ===
None
=== RETURN VALUE ===
None
*/
void drawTarg()
{
  //draw targ
  if (targAlive)
  {
    fill(255, 0, 0);
    textFont(targFont, 20);
    textAlign(CENTER, CENTER);
    text("if(x!=y){\nnull++}\n//err",
      targHitX + targHitW/2,
      targHitY + targHitH/2);
  }
}

/* void mousePressed()
=== FUNCTION DESCRIPTION ===
allows the mouse to click within a certain range (the coords of the play again button)
=== PARAMETERS ===
None
=== RETURN VALUE ===
None
*/
void mousePressed()
{
  if (gameOver)
  {
    if (mouseX > 425 && mouseX < 575 && mouseY > 325 && mouseY < 365)
    {
      resetGame();
    }
  }
}

/* void resetGame()
=== FUNCTION DESCRIPTION ===
sets player, enemy, and targ values to starting value
=== PARAMETERS ===
None
=== RETURN VALUE ===
None
*/
void resetGame()
{
  hitX = width/2 - hitW/2;
  hitY = height/2 + 170;
  targHitX = width/2 - targHitW/2 + 10;
  targHitY = height/3.5;
  targAlive = true;
  coinActive = false;
  coinCount = 0;
  fireActive = false;
  gameOver = false;
  gameWon = false;
  gameLost = false;
  
  for (int i=0; i<10; i++) {
    enemyX[i] = int(random(0, width - enemySize[i]));
    enemyY[i] = 0;
    enemySpeed[i] = int(random(2, 8));
  }
  // allow the game to start again
}

/* void setup()
=== FUNCTION DESCRIPTION ===
creates player starting hitbox and enemy starting positions
=== PARAMETERS ===
None
=== RETURN VALUE ===
None
*/
void setup()
{
  size(1000, 750); //screen size

  hitX = width/2 - hitW/2;
  hitY = height/2 + 170;
  targHitX = width/2 - targHitW/2+10;
  targHitY = height/3.5;
  targFont = createFont("Courier", 12);

  //initialize enemy variables
  for (int i=0; i<10; i++)
  {
    enemySize[i] = 30;
    enemyX[i] = int(random(0, width-enemySize[i]));
    enemyY[i] = 0;
    enemySpeed[i] = int (random (2, 8));
  }
}

/* void gameOverScreen()
=== FUNCTION DESCRIPTION ===
sets game over and lose condition both to true when 
an enemy touches the player
=== PARAMETERS ===
None
=== RETURN VALUE ===
None
*/
void gameOverScreen()
{
  if (enemyCollision())
  {
    println("YOU CANNOT NOT PASS");
    gameOver = true;
    gameLost = true;
  }
}

/* void draw()
=== FUNCTION DESCRIPTION ===
calls the nessesary functions 
=== PARAMETERS ===
None
=== RETURN VALUE ===
None
*/
void draw()
{
  drawBackground(); //creates the background (sky, clouds, coin bar, etc.)

  drawPlayer(); //creates the player, Setup Wizard
  playerMovement(); //calls the player movement function
  playerFire(); //includes fireball design & logic

  if (!gameOver)
  {
    enemies();
    moveEnemies();
  }

  drawTarg();
  moveTarg();
  targCollision();
  
  drawCoin();
  drawCoinBar();

  drawPlayAgainButton();

  gameOverScreen();
  gameWonScreen();
  gameLostScreen();
}
