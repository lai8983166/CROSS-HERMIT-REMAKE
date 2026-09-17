
void __fastcall FUN__text__004144e0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [15];
  undefined4 uStack_18;
  int local_14;
  int *local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (int *)0x0;
  local_10 = (int *)0x0;
  local_8 = param_1;
  (**(code **)(**(int **)(param_1 + 0xb210) + 0x40))(*(undefined4 *)(param_1 + 0xb210),0,0,&local_c)
  ;
  local_14 = FUN__text__0056ce80();
  if (-1 < local_14) {
    (**(code **)(**(int **)(local_8 + 0xb210) + 0x84))(*(undefined4 *)(local_8 + 0xb210),&local_10);
    local_14 = FUN__text__0056ce80();
    if (local_14 == -0x7789f79a) {
      local_10 = (int *)0x0;
    }
    else if (local_14 < 0) goto LAB__text__004145f5;
    (**(code **)(**(int **)(local_8 + 0xb210) + 0x7c))
              (*(undefined4 *)(local_8 + 0xb210),local_c,local_10);
    local_14 = FUN__text__0056ce80();
    if (local_c != (int *)0x0) {
      (**(code **)(*local_c + 8))(local_c);
      FUN__text__0056ce80();
    }
    if (local_10 != (int *)0x0) {
      (**(code **)(*local_10 + 8))(local_10);
      FUN__text__0056ce80();
    }
  }
LAB__text__004145f5:
  uStack_18 = 0x414602;
  FUN__text__0056ce80();
  return;
}

