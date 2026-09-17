
void __thiscall FUN__text__0046efa0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = 0;
  local_8 = param_1;
  do {
    if (local_c == *(int *)(local_8 + 0xdc30c)) {
LAB__text__0046f157:
      local_8 = 0x46f164;
      FUN__text__0056ce80();
      return;
    }
    iVar1 = FUN__text__00468d10(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
    if ((iVar1 != 0) &&
       (iVar1 = FUN__text__00468f40(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4)), iVar1 != 0))
    {
      if (param_2 == 0) {
        local_10 = FUN__text__0046fc20(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
      }
      else {
        local_10 = FUN__text__0046fd70(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
      }
      if (local_10 != 0) {
        if ((*(uint *)(DAT_007a49fc + 0x194c) & 0x40000) == 0) {
          *(undefined1 *)(*(int *)(local_8 + 0xdc310 + local_c * 4) + 0x28c) = 1;
        }
        else {
          *(byte *)(*(int *)(local_8 + 0xdc310 + local_c * 4) + 0x28c) =
               *(byte *)(*(int *)(local_8 + 0xdc310 + local_c * 4) + 0x28c) ^ 1;
        }
        *(int *)(local_8 + 0x108f74) = *(int *)(local_8 + 0x108f74) + 1;
        if (param_2 == 0) {
          iVar1 = FUN__text__00469480(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
          if ((((iVar1 != 0) &&
               (iVar1 = FUN__text__0046a4c0(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4)),
               iVar1 != 0)) && ((*(uint *)(DAT_007a49fc + 0x1990) & 0x40) != 0)) &&
             (((*(uint *)(DAT_007a49fc + 0x194c) & 0x40000) == 0 &&
              (*(char *)(local_8 + 0x108b36) != '\0')))) {
            FUN__text__00494a50(*(undefined4 *)(local_8 + 0xdc310 + local_c * 4));
          }
          goto LAB__text__0046f157;
        }
      }
    }
    local_c = local_c + 1;
  } while( true );
}

