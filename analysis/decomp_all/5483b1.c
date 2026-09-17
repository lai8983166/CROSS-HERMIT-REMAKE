
void __fastcall FUN__text__005483b1(undefined4 *param_1)

{
  undefined4 *puVar1;
  int iVar2;
  
  *param_1 = 1;
  param_1[1] = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  puVar1 = param_1 + 0xc;
  iVar2 = 8;
  do {
    puVar1[-8] = 0;
    *puVar1 = 0;
    puVar1 = puVar1 + 1;
    iVar2 = iVar2 + -1;
  } while (iVar2 != 0);
  param_1[0x18] = 0;
  param_1[0x19] = 0;
  param_1[0x1a] = 0;
  param_1[0x26] = 0;
  param_1[0x27] = 0;
  param_1[0x2a] = 0;
  param_1[0x1b] = 0;
  param_1[0x2b] = 0;
  return;
}

