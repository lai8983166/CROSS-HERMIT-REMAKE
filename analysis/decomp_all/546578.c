
void FUN__text__00546578(int param_1,undefined4 param_2,undefined4 param_3)

{
  if (*(code **)(param_1 + 0x50) != (code *)0x0) {
    (**(code **)(param_1 + 0x50))(param_1,param_2,param_3);
    return;
  }
  FUN__text__0054381d(param_1,"Call to NULL read function");
  return;
}

