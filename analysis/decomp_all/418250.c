
void __fastcall FUN__text__00418250(int *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*param_1 != 0) && (param_1[0x5d] != 0)) {
    local_8 = param_1;
    FUN__text__0042b2d0("DirectPlay:ServiceProvider\n");
    for (local_c = 0; local_c != local_8[0x5d]; local_c = local_c + 1) {
      FUN__text__0042b2d0("%03d:%s\n",local_c,local_8[local_c * 5 + 0x62]);
    }
  }
  local_8 = (int *)0x4182e3;
  FUN__text__0056ce80();
  return;
}

