
void FUN__text__00493960(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__004938d0();
  if (local_c != 0) {
    *(undefined1 *)(local_c + 1) = (undefined1)param_3;
    local_10 = local_c + 4;
    *(int *)(local_c + 0x2f0) = param_1 << 0x10;
    *(int *)(local_c + 0x2f4) = param_2 << 0x10;
    if (param_3 == 0) {
      FUN__text__00409ff0(local_c + 0x4c,0,0x2d,0);
      FUN__text__004db2b0(10);
    }
    else {
      FUN__text__00409ff0(local_c + 0x4c,3,0x87,0);
      FUN__text__004db2b0(0xb);
    }
  }
  local_8 = 0x493a1c;
  FUN__text__0056ce80();
  return;
}

