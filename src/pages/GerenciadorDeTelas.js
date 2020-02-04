import { createAppContainer, createSwitchNavigator } from 'react-navigation';
import { createStackNavigator } from 'react-navigation-stack';
import TelaLogin from "./TelaLogin";
import TelaPainel from "./TelaPainel";

const AppStackPainel = createStackNavigator({ Painel: TelaPainel });
const ContainerStackPainel = createAppContainer(AppStackPainel);
const AuthStack = createStackNavigator({ Login: TelaLogin });
const ContainerAuthStack = createAppContainer(AuthStack);
const SwitchNavigator = createSwitchNavigator(
    {
      Auth: ContainerAuthStack,
      App: ContainerStackPainel,
    }
  );
export default createAppContainer(SwitchNavigator);
