
void __fastcall FUN__text__00425800(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  *(undefined1 *)((int)param_1 + 0x15) = 0;
  param_1[0x18a] = 0x100;
  param_1[0x18b] = 0x100;
  param_1[0x18e] = 0x40;
  local_8 = param_1;
  FUN__text__00426110();
  FUN__text__00426190();
  FUN__text__00426250();
  *(undefined1 *)(local_8 + 0x18c) = 0;
  local_8 = (undefined4 *)0x4258ad;
  FUN__text__0056ce80();
  return;
}

