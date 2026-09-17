
void __fastcall FUN__text__004373a0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  FUN__text__004313f0(param_1 + 0x115d14);
  if ((*(short *)(local_8 + 0x115e2c) == 0) && (*(short *)(local_8 + 0x115e32) == 0)) {
    *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 1;
    FUN__text__004549d0(0,0,0,1,0,0,1);
  }
  else {
    local_c = FUN__text__00431890(local_8 + 0x115d14);
    if (local_c == 0) {
      if (*(int *)(local_8 + 0x2e6f4) == 0) {
        *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
        FUN__text__004549d0(0,0,0,1,0,0,1);
      }
    }
    else {
      *(undefined4 *)(*(int *)(local_8 + 0x117c38) + 0x174) = 5;
      FUN__text__004549d0(0,0,0,1,0,0,1);
    }
  }
  local_8 = 0x4374bc;
  FUN__text__0056ce80();
  return;
}

