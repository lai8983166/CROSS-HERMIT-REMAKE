
void FUN__text__004263b0(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (DAT_0079fc68 == 0) {
    iVar2 = FUN__text__00425c70();
    if (iVar2 != 0) {
      if (*(char *)(local_8 + 0x15) == '\0') {
        (*API_KERNEL32_DLL_lstrlenA)(local_8 + 0x528);
        local_c = FUN__text__0056ce80();
        if (local_c == 0) {
          if (param_1 != 0) {
            iVar2 = FUN__text__004128f0(0xe,2);
            if (iVar2 == 0) {
              iVar2 = FUN__text__004128f0(0x1c,1);
              if (iVar2 != 0) {
                (*API_KERNEL32_DLL_lstrlenA)(local_8 + 0x63c);
                FUN__text__0056ce80();
              }
            }
            else {
              FUN__text__00426640();
            }
          }
        }
        else {
          uVar1 = FUN__text__00426040();
          *(undefined4 *)(local_8 + 0x634) = uVar1;
        }
      }
      else {
        *(char *)(local_8 + 0x15) = *(char *)(local_8 + 0x15) + -1;
      }
    }
  }
  else {
    DAT_0079fc68 = 0;
  }
  local_8 = 0x4264be;
  FUN__text__0056ce80();
  return;
}

